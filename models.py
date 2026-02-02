from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

class Candidate(db.Model):
    """
    Table to store candidate details.
    """
    __tablename__ = 'candidates'

    # 1. Identity
    id = db.Column(db.Integer, primary_key=True)
    
    # 2. Display Info
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    # 3. The "Link" to your Local S3
    # Stores: 'static/resumes/filename.pdf'
    file_path = db.Column(db.String(200), nullable=False)
    
    # 4. The Raw Data (for display or re-processing)
    text = db.Column(db.Text, nullable=True)
    
    # 5. The "Brain" Data (The NLP Vector)
    # We store the list of numbers as a "Pickle" (binary object)
    # This makes retrieval instant.
    vector = db.Column(db.PickleType, nullable=True)

    def __repr__(self):
        return f'<Candidate {self.name}>'