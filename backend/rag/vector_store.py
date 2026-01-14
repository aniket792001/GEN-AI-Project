import os
import shutil
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "faiss_index"

def load_documents(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file format")

    return loader.load()

def create_vector_store(file_path: str):
    documents = load_documents(file_path)

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=40
    )


    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)

def reset_vector_store():
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)
