# AI Resume Screening System

An intelligent resume screening and candidate ranking platform that helps recruiters quickly identify the most suitable candidates for a job role. The system uses Natural Language Processing (NLP) and Machine Learning techniques to analyze resumes, compare them against job descriptions, and generate ranked results based on relevance and skill matching.

## Project Overview

Recruiters often spend significant time manually reviewing resumes, especially when hiring for highly competitive positions. This project automates the initial screening process by evaluating candidate resumes against a given job description and ranking them according to their suitability.

The application leverages TF-IDF vectorization and Cosine Similarity to measure how closely a resume matches the requirements of a role. It also extracts relevant keywords, highlights matched skills, and provides a clear ranking system to simplify candidate shortlisting.

The project follows a full-stack architecture with a Flask backend, React frontend, REST APIs, automated testing, and a modular design that promotes maintainability and scalability.

---

## Problem Statement

Traditional resume screening is:

- Time-consuming
- Repetitive
- Prone to human bias
- Difficult to scale for large applicant pools

This project addresses these challenges by providing an automated and data-driven approach to candidate evaluation, enabling recruiters to focus on the most relevant applicants.

---

## Key Features

### Resume Processing
- Upload multiple resumes simultaneously
- Supports PDF and TXT file formats
- Automatic text extraction and parsing
- Candidate identification from uploaded files

### NLP-Based Analysis
- Text cleaning and normalization
- Tokenization
- Stop-word removal
- Lemmatization
- Keyword extraction

### Intelligent Candidate Matching
- TF-IDF Vectorization
- Cosine Similarity Scoring
- Keyword overlap detection
- Context-based relevance matching

### Candidate Ranking
- Resume scoring based on job requirements
- Automatic ranking from best match to lowest match
- Skill match visualization
- Candidate comparison support

### Analytics Dashboard
- Total resumes screened
- Highest score
- Average score
- Lowest score
- Score distribution metrics

### User Experience
- Modern and responsive React interface
- Drag-and-drop file upload
- Real-time processing feedback
- Expandable candidate details
- Clean and intuitive UI

### Reliability
- Comprehensive unit testing
- API validation
- Error handling
- Health monitoring endpoint

---

## Technology Stack

### Backend
- Python
- Flask
- Flask-CORS
- Scikit-Learn
- NLTK
- NumPy
- PyPDF2
- Pytest

### Frontend
- React
- Vite
- JavaScript
- CSS

### Machine Learning & NLP
- TF-IDF Vectorizer
- Cosine Similarity
- Tokenization
- Lemmatization
- Keyword Extraction

---

## System Workflow

```text
Job Description
       │
       ▼
NLP Preprocessing
(Cleaning, Tokenization, Lemmatization)
       │
       ▼
TF-IDF Vectorization
       │
       ▼
Cosine Similarity Calculation
       │
       ▼
Resume Scoring
       │
       ▼
Candidate Ranking
       │
       ▼
Results & Analytics Dashboard
```

---

## How It Works

### 1. Job Description Input
The recruiter enters a job title and job description containing the required skills and qualifications.

### 2. Resume Upload
Multiple resumes can be uploaded in PDF or TXT format.

### 3. Text Processing
The system preprocesses both resumes and job descriptions by:
- Removing noise and irrelevant characters
- Tokenizing text into meaningful words
- Removing stop words
- Applying lemmatization

### 4. Feature Extraction
TF-IDF converts text into numerical vectors that represent the importance of terms within documents.

### 5. Similarity Analysis
Cosine Similarity compares each resume with the job description and generates a relevance score.

### 6. Candidate Ranking
Candidates are ranked from highest to lowest score, helping recruiters identify the strongest matches instantly.

---

## Why TF-IDF and Cosine Similarity?

### TF-IDF
TF-IDF (Term Frequency-Inverse Document Frequency) helps identify important keywords while reducing the influence of commonly occurring words.

Benefits:
- Better keyword importance detection
- Reduced noise
- Improved text representation

### Cosine Similarity
Cosine Similarity measures the similarity between two text vectors.

Benefits:
- Effective for text comparison
- Works well with sparse data
- Produces interpretable similarity scores

Together, these techniques provide a lightweight yet effective approach for resume ranking.

---

## Project Structure

```bash
ai-resume-screener/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   ├── routes/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
└── sample_resumes/
```

---

## API Endpoints

### Health Check

```http
GET /api/health
```

### Screen Resumes

```http
POST /api/screen
```

Required Fields:

```text
job_title
job_description
resumes[]
```

### Sample Job Description

```http
GET /api/sample-jd
```

---

## Running the Project

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

python run.py
```

Backend will run on:

```text
http://localhost:5000
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend will run on:

```text
http://localhost:3000
```

---

## Running Tests

```bash
cd backend

pytest tests/ -v
```

The project includes extensive test coverage for:

- NLP preprocessing
- Resume parsing
- Similarity scoring
- Candidate ranking
- Statistical analysis
- Data models

---

## Example Use Case

### Job Role
Senior Python Developer

### Required Skills
- Python
- Flask
- Django
- REST APIs
- PostgreSQL
- Docker
- AWS
- Scikit-Learn

### Expected Result

| Rank | Candidate | Outcome |
|--------|-----------|----------|
| 1 | Alice Johnson | Best Match |
| 2 | Priya Sharma | Strong Match |
| 3 | Bob Martinez | Partial Match |

The system automatically identifies the most relevant candidates based on skills, experience, and overall job relevance.

---

## Future Enhancements

Planned improvements include:

- DOCX resume support
- OCR-based resume extraction
- BERT-based semantic matching
- Candidate recommendation engine
- Skill-gap analysis
- Authentication and user management
- Database integration
- Export reports to PDF/Excel
- ATS integration

---

## Learning Outcomes

This project provided practical experience in:

- Natural Language Processing
- Machine Learning for text analysis
- Full-Stack Web Development
- REST API Development
- React Application Architecture
- Flask Backend Development
- Automated Testing with Pytest
- Software Design Principles
- Recruitment Technology Solutions

---

## Final Thoughts

This project demonstrates how Artificial Intelligence and Natural Language Processing can be applied to streamline recruitment workflows. By automating resume screening and candidate ranking, the system helps reduce manual effort, improve efficiency, and support more informed hiring decisions.

Beyond solving a real-world problem, the project also emphasizes clean architecture, maintainable code, scalability, and industry-standard development practices.

If you found this project helpful, consider giving it a ⭐ on GitHub.
Feedback, suggestions, and contributions are always welcome.
