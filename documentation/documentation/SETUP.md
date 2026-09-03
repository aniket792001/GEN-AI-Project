# Local Setup Guide

## Prerequisites
- Python 3.10+ recommended
- Git

## 1. Clone and create a virtual environment
```bash
git clone https://github.com/aniket792001/GEN-AI-Project.git
cd GEN-AI-Project

python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
```

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. (First run only) Start with a clean index
If you're testing from scratch, make sure no old `faiss_index/` folder exists — the backend will
build one automatically on the first document upload.

## 4. Start the backend
```bash
uvicorn backend.main:app --reload
```
Visit `http://127.0.0.1:8000` — you should see `{"status": "RAG backend running"}`.

## 5. Start the frontend (in a separate terminal, venv activated)
```bash
streamlit run frontend/app.py
```
This opens the chat UI in your browser, typically at `http://localhost:8501`.

## 6. Test the flow
1. Upload a PDF/DOCX/TXT file using the uploader
2. Wait for "Document indexed successfully"
3. Ask a question about the document's content
4. Confirm the answer includes a citation to the uploaded filename
5. Try "Reset Knowledge Base" and confirm it succeeds and clears the index

## Troubleshooting
| Symptom | Likely Cause | Fix |
|---|---|---|
| `pip install` fails on a package name | Stale `requirements.txt` with an invalid entry | Confirm you're using the fixed `requirements.txt` (no `react-native` line) |
| Backend crashes on startup | Old code trying to load a FAISS index that doesn't exist yet | Confirm you're using the fixed `qa_chain.py` with lazy loading |
| "Reset Knowledge Base" button errors | Old `main.py` without the `/reset` route | Confirm you're using the fixed `main.py` |
| Answers seem to ignore an earlier uploaded document | Old `vector_store.py` that overwrites instead of merges | Confirm you're using the fixed `vector_store.py` |
| Slow responses | Expected — CPU inference with `flan-t5-base` | See ROADMAP.md for the hosted-API swap plan |
