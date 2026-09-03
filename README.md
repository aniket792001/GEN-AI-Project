# FinDocs QA — RAG Assistant for Financial & Loan Document Search

A Retrieval-Augmented Generation (RAG) system that lets users ask natural-language questions
over financial and loan-related documents (agreements, policy PDFs, terms & conditions) and get
**context-grounded answers with source citations** — instead of manually searching through pages
of dense text.

## Problem

Fintech and lending teams generate large volumes of document-heavy content — loan agreements,
policy documents, compliance PDFs — that customer support agents, field staff, and even customers
need to reference constantly. Manually searching these documents for a specific clause or answer
is slow and error-prone. This project was inspired by that exact workflow, seen while building a
production fintech micro-financing platform (Project Pebble, 1GEN).

## What It Does

- Upload PDF, DOCX, or TXT documents (e.g., loan terms, policy documents)
- Ask questions in plain language and get answers generated **only from the retrieved document
  context** (not the model's general knowledge), reducing hallucination
- Every answer includes **source citations** so users can verify the answer against the original
  document
- Multi-document support — upload multiple documents and query across all of them
- Simple Streamlit chat interface for non-technical users; FastAPI backend for integration into
  other systems

## Architecture

```
Upload (PDF/DOCX/TXT)
      │
      ▼
Document Loader  →  Chunking (RecursiveCharacterTextSplitter)
      │
      ▼
Embeddings (Hugging Face: all-MiniLM-L6-v2)
      │
      ▼
FAISS Vector Store  ──────────────►  Similarity Search (top-k retrieval)
                                              │
                                              ▼
                                   LLM Answer Generation
                                   (context-restricted prompt)
                                              │
                                              ▼
                                Answer + Source Citations
```

## Tech Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **LLM Framework:** LangChain
- **Embeddings:** Hugging Face (`sentence-transformers/all-MiniLM-L6-v2`)
- **Vector Store:** FAISS
- **Generation Model:** `google/flan-t5-base` (CPU inference)

## Project Structure
```text
GEN-AI-Project/
├── backend/
│   ├── main.py              # FastAPI entry point (/upload, /ask, /reset)
│   └── rag/
│       ├── loader.py        # Document loading (PDF/DOCX/TXT)
│       ├── splitter.py      # Chunking logic
│       ├── embeddings.py    # Embedding model config
│       ├── vector_store.py  # FAISS index creation, loading, reset
│       └── qa_chain.py      # RAG retrieval + generation pipeline
├── frontend/
│   └── app.py               # Streamlit chat UI
├── faiss_index/             # Saved FAISS vector database
├── uploads/                 # Uploaded source documents
├── requirements.txt
└── README.md
```

## Installation & Setup

```bash
git clone https://github.com/aniket792001/GEN-AI-Project.git
cd GEN-AI-Project

python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

## Running the Application

**Start the backend:**
```bash
uvicorn backend.main:app --reload
```
Runs at `http://127.0.0.1:8000`

**Start the frontend (separate terminal):**
```bash
streamlit run frontend/app.py
```

## API Endpoints

**Upload a document**
```
POST /upload
```

**Ask a question**
```
POST /ask
Body: { "question": "What is the late payment penalty in the agreement?" }

Response:
{
  "answer": "The late payment penalty is ...",
  "citations": ["loan_agreement.pdf"]
}
```

**Reset the knowledge base**
```
POST /reset
```

## How It Works (RAG Flow)
1. Documents are split into overlapping chunks
2. Chunks are embedded using a Hugging Face sentence-transformer model
3. FAISS stores embeddings for fast similarity search
4. On a question, the most relevant chunks are retrieved
5. The LLM generates an answer using **only** the retrieved context — explicitly instructed to
   say "I don't know" rather than hallucinate when the answer isn't present
6. Source document citations are returned alongside the answer

## Known Limitations
- Generation model (`flan-t5-base`) has a limited effective context window; retrieved context is
  currently truncated to ~1200 characters to stay within it
- Runs on CPU — inference is slower than a GPU or hosted-API setup, and realistically supports
  only a handful of concurrent users
- Citations currently reference the source file, not the specific page or paragraph

## Planned Improvements
- Swap to a hosted LLM API (Gemini/OpenAI) to remove the context-window constraint and improve
  concurrent scale
- Page-level citations instead of file-level
- Conversation memory for multi-turn follow-up questions
- Deployment (Render/Railway) with a hosted vector DB for horizontal scaling
- Basic retrieval evaluation set to measure and tune answer quality

## Author
Aniket Kadam
B.Tech — Artificial Intelligence & Data Science
AI/GenAI Engineer

## Acknowledgements
LangChain · Hugging Face · FAISS · FastAPI · Streamlit