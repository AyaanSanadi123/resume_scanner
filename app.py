import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, Candidate
from utils import extract_text_from_pdf, get_embedding
from sentence_transformers import util  # <--- For calculating the score

app = Flask(__name__)

# --- Configuration ---
app.config['UPLOAD_FOLDER'] = 'static/resumes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_screener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure folders exist
with app.app_context():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.create_all()

# --- Routes ---

@app.route('/')
def home():
    """Renders the dashboard/search page."""
    return render_template('search.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'GET':
        return render_template('upload.html')

    # 1. Get the Manual Inputs
    name = request.form.get('name')
    email = request.form.get('email')
    file = request.files.get('resume') # Changed from 'resumes' to 'resume'

    if not file or not name:
        return "Missing data", 400

    # 2. Save the File
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # 3. AI Processing
    text = extract_text_from_pdf(file_path)
    vector = get_embedding(text)

    # 4. Save to DB (With Name and Email)
    new_candidate = Candidate(
        name=name,       # User input
        email=email,     # User input
        file_path=file_path,
        text=text,
        vector=vector
    )
    db.session.add(new_candidate)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/search', methods=['POST'])
def search():
    """
    The Core Ranking Logic.
    """
    query = request.form.get('query')
    if not query:
        return redirect(url_for('home'))

    # 1. Convert User's Query to Vector
    query_vector = get_embedding(query)

    # 2. Get All Candidates
    candidates = Candidate.query.all()
    results = []

    for candidate in candidates:
        if candidate.vector is None:
            continue
            
        # 3. Compare Query Vector vs Candidate Vector (Cosine Similarity)
        # Returns a score between 0.0 and 1.0
        score = util.cos_sim(query_vector, candidate.vector).item()
        
        results.append({
            'candidate': candidate,
            'score': round(score * 100, 2)  # Convert to percentage
        })

    # 4. Sort by Highest Score
    results.sort(key=lambda x: x['score'], reverse=True)

    # 5. Render the Results
    return render_template('search.html', results=results, query=query)

@app.route('/candidate/<int:id>')
def candidate_detail(id):
    """Shows the detailed view of a single candidate"""
    candidate = Candidate.query.get_or_404(id)
    return render_template('candidate.html', candidate=candidate)

if __name__ == '__main__':
    app.run(debug=True)