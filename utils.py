import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

# --- LOAD AI MODEL ONCE ---
# We load the model here so it stays in memory. 
# This makes processing resumes very fast after the initial startup.
print("Loading AI Model... (This may take 2-3 seconds)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("AI Model Loaded and Ready!")

def extract_text_from_pdf(file_path):
    """
    Opens a PDF file and returns all the text inside it as a single string.
    """
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def get_embedding(text):
    """
    Converts a string of text into a list of numbers (Vector).
    """
    if not text:
        return []
    
    # 1. Convert text to vector using the AI model
    # This returns a "Numpy Array" which databases can't store easily.
    vector_array = model.encode(text)
    
    # 2. Convert Numpy Array -> Python List
    # SQLite loves Python Lists (especially with the PickleType we used).
    return vector_array.tolist()