# FastAPI Books API
A simple FastAPI application to manage books with CRUD operations.

## Requirements
- **Python:** 3.10+
- **Database:** SQLite
- **Packages:** fastapi, uvicorn, pytest, httpx

## How to Run
Clone the repository and navigate to the project folder:
```bash
git clone <repo-url>
cd <project-folder>
```

Install dependencies:
```bash
python -m pip install --upgrade pip
python -m pip install fastapi[all] pytest httpx
```

Run the FastAPI app:
```bash
uvicorn main:app --reload
```

Access the API:  
- URL: `http://127.0.0.1:8000`  
- Swagger Docs: `http://127.0.0.1:8000/docs`

## How to Test
**Unit Tests (mocked DB):**
```bash
python -m pytest -v test_app_unit.py
```

**Integration Test (real DB):**
```bash
python -m pytest -v test_app_integration.py
```

## Suggested Improvements for Production
**Database Improvements:**
- Use a real production database (PostgreSQL/MySQL) instead of in-memory or SQLite
- Apply stricter validation of inputs
- Provide more informative error messages

**Logging & Monitoring:**
- Log requests and errors
- Sanitize inputs to prevent SQL injection
- Apply authentication and authorization

**Deployment:**
- Containerize using Docker for reproducible environments
- Use a production-ready server like Gunicorn or Uvicorn with workers

