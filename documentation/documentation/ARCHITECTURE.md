# Architecture

## Overview
This project implements a Retrieval-Augmented Generation (RAG) pipeline for document Q&A,
split into a FastAPI backend and a Streamlit frontend.

## Data Flow

```
User uploads document (PDF/DOCX/TXT)
        │
        ▼
backend/rag/loader.py        → loads raw text from the file using the correct parser
        │
        ▼
backend/rag/splitter.py      → splits text into overlapping chunks
        │
        ▼
backend/rag/embeddings.py    → converts each chunk into a vector embedding
        │
        ▼
backend/rag/vector_store.py  → stores/merges embeddings into a local FAISS index
        │
        ▼
   [ FAISS index persisted to disk: faiss_index/ ]


User asks a question
        │
        ▼
backend/rag/qa_chain.py:
   1. Embed the question (same embedding model as above)
   2. Retrieve top-k most similar chunks from FAISS
   3. Truncate/assemble retrieved chunks into a context string
   4. Pass context + question into the LLM prompt template
   5. LLM generates an answer restricted to the provided context
        │
        ▼
   Answer + source citations returned to the frontend
```

## Component Responsibilities

| Module | Responsibility |
|---|---|
| `backend/main.py` | FastAPI routes: `/upload`, `/ask`, `/reset`. Orchestrates the pipeline, holds no business logic itself. |
| `backend/rag/loader.py` | Reads PDF/DOCX/TXT files into LangChain `Document` objects. |
| `backend/rag/splitter.py` | Single source of truth for chunking config (chunk size, overlap). |
| `backend/rag/embeddings.py` | Single source of truth for the embedding model used everywhere (indexing AND querying must use the same model). |
| `backend/rag/vector_store.py` | Creates, loads, merges, and resets the FAISS index. |
| `backend/rag/qa_chain.py` | The actual RAG "ask" logic: retrieval + prompt assembly + generation. |
| `frontend/app.py` | Streamlit UI: upload button, chat interface, reset button. Talks to the backend only via HTTP — has no direct access to the RAG pipeline. |

## Why These Design Choices

- **Local FAISS instead of a hosted vector DB:** zero cost, no external account needed, good for a
  single-user/demo setting. Tradeoff: doesn't scale horizontally across multiple backend instances.
- **`flan-t5-base` running on CPU instead of a hosted LLM API:** zero API cost, full control,
  works offline. Tradeoff: small effective context window, slow inference, limited concurrency.
- **Shared `embeddings.py` module:** the same embedding model MUST be used for both indexing
  (when a document is uploaded) and querying (when a question is asked) — otherwise similarity
  search breaks. Centralizing this in one file prevents that class of bug.
- **Context-restricted prompting:** the LLM is explicitly told to say "I don't know" rather than
  answer from its own general knowledge, to reduce hallucination and keep answers grounded in the
  uploaded documents.

## Known Architectural Limits (see also KNOWN_ISSUES.md)
- Single-process, single-model-instance design — not designed for concurrent production traffic
- FAISS index lives on local disk — not shared across multiple server instances
- No caching layer — identical questions are recomputed from scratch every time
