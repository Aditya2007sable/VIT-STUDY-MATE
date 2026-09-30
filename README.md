# VIT-STUDY-MATE

VIT StudyMate is an AI-powered academic learning assistant for studying from a student's own course PDFs.

Course: Introduction to problem solving 1021

Repository: https://github.com/Aditya2007sable/VIT-STUDY-MATE

## Features
1. Upload/Add Module — extracts PDF text and stores it in SQLite.
2. Ask StudyMate — answers using retrieved content from the selected uploaded module.
3. Generate Quiz — creates MCQs from the selected module and records scores.
4. View Performance — calculates quiz attempts, averages and best scores.
5. Assignment Manager — stores and displays assignments.
6. Study Planner — creates a simple subject-wise daily plan.
7. View Modules — lists every uploaded module directly from SQLite.

## Technology
- Python
- SQLite
- OpenAI API
- PyPDF
- python-dotenv
- pytest

## Setup

### 1. Create virtual environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install packages
```powershell
python -m pip install -r requirements.txt
```

### 3. Configure OpenAI
Copy `.env.example` to `.env` and add your API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-6-luna
```

Never commit `.env` to GitHub.

### 4. Run
```powershell
python app.py
```

## Testing
```powershell
pytest -q
```

## AI knowledge boundary
The tutor and quiz prompts instruct the AI to use only the supplied uploaded-module context. StudyMate does not enable web search.

## Architecture
PDF -> PyPDF text extraction -> SQLite -> module retrieval -> OpenAI -> Tutor/Quiz

Local features such as Performance, Assignments, Study Planner and View Modules work without an AI API call.
