# 🚀 Smart Resume Screener

An AI-powered tool that ranks resumes based on their relevance to a job description. Unlike simple keyword matching, this system uses **Machine Learning (NLP)** to understand the *meaning* (semantics) of the resume text.

## ✨ Features
* **AI-Powered Ranking:** Uses the `all-MiniLM-L6-v2` transformer model to convert text into high-dimensional vectors.
* **Semantic Search:** Finds candidates based on context, not just exact keywords (e.g., matches "Coder" to "Programmer").
* **PDF Parsing:** Automatically extracts text from uploaded PDF resumes.
* **Clean Dashboard:** A user-friendly interface built with Bootstrap for uploading and screening candidates.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite (local file storage)
* **AI/ML:** Sentence-Transformers (BERT), Scikit-Learn (Cosine Similarity)
* **PDF Processing:** PyMuPDF
* **Frontend:** HTML5, Bootstrap 5

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/resume-screener.git](https://github.com/YOUR_USERNAME/resume-screener.git)
    cd resume-screener
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python app.py
    ```

5.  **Open in Browser**
    Go to `http://127.0.0.1:5000`

## 📖 How It Works
1.  **Upload:** When a resume (PDF) is uploaded, the text is extracted and passed through the **Sentence-BERT** model.
2.  **Vectorization:** The model converts the text into a **384-dimensional vector** (a list of numbers representing the meaning).
3.  **Storage:** The vector and text are stored in the SQLite database.
4.  **Search:** When you enter a Job Description, it is also converted into a vector.
5.  **Ranking:** The system calculates the **Cosine Similarity** score between the Job Description vector and every candidate's vector to rank them from 0% to 100% match.
