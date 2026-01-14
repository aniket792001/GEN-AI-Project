from fastapi import FastAPI, UploadFile, File
import os
import shutil

from backend.rag.vector_store import create_vector_store
from backend.rag.qa_chain import get_rag_chain

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"status": "RAG backend running"}


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    create_vector_store(file_path)

    return {"message": "Document processed successfully"}



rag_chain = get_rag_chain()

@app.post("/ask")
def ask_question(req: dict):
    result = rag_chain(req["question"])
    return {
    "answer": result["answer"],
    "citations": result.get("sources", [])
    }

