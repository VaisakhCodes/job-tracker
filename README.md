# Job Tracker AI

A full-stack job application tracker with an AI-powered job description analyser.

**Live Demo:** https://job-tracker-yxs2.onrender.com/login.html  
**GitHub:** https://github.com/VaisakhCodes/job-tracker

## Features

- Track job applications with status pipeline (Applied → Interview → Offer)
- JWT authentication — register, login, protected routes
- AI-powered JD analyser — paste a job description and get a fit score, matched keywords, and missing skills
- REST API backend with FastAPI and SQLAlchemy
- Deployed on Render with Docker

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, JWT, bcrypt  
**AI/NLP:** spaCy, scikit-learn (TF-IDF cosine similarity)  
**Database:** SQLite (local), PostgreSQL (production)  
**Frontend:** HTML5, Tailwind CSS, Vanilla JS  
**Infrastructure:** Docker, Render, GitHub

## Running Locally

```bash
git clone https://github.com/VaisakhCodes/job-tracker.git
cd job-tracker/backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/login.html`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Create account |
| POST | /auth/login | Get JWT token |
| GET | /applications/ | List all applications |
| POST | /applications/ | Add application |
| PATCH | /applications/{id} | Update status |
| DELETE | /applications/{id} | Delete application |
| POST | /analyse/ | Analyse JD fit score |

## Project Structure

```
job-tracker/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── models.py        # Database tables
│   ├── auth.py          # JWT authentication
│   ├── routers/         # API endpoints
│   └── nlp/             # spaCy + TF-IDF analyser
└── frontend/
    ├── login.html       # Auth page
    ├── index.html       # Dashboard
    └── analyser.html    # JD analyser
```