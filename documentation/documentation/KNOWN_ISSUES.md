# Known Issues & Fix History

## Fixed

| Issue | Description | Fixed In |
|---|---|---|
| Invalid dependency | `react-native` (an npm package) was listed in `requirements.txt`, breaking `pip install -r requirements.txt` on a fresh clone | `requirements.txt` |
| Missing `/reset` route | Frontend's "Reset Knowledge Base" button called `POST /reset`, but no such route existed in `main.py`, causing a runtime error on click | `backend/main.py` |
| Startup crash with no index | `get_rag_chain()` was called at import time and immediately tried to load a FAISS index from disk — if no document had ever been uploaded, the app crashed on startup instead of starting cleanly | `backend/rag/qa_chain.py` (lazy init) |
| Second upload erases first document | `create_vector_store()` always built a brand-new FAISS index (`FAISS.from_documents`) instead of checking for an existing one, so uploading a second document silently deleted the first document's embeddings | `backend/rag/vector_store.py` (merge logic added) |
| Duplicate, inconsistent chunking config | `splitter.py` (chunk_size=800) was dead code — `vector_store.py` had its own inline splitter with different values (chunk_size=300), so the "real" chunk size wasn't obvious from reading the codebase | Consolidated into `splitter.py`, imported by `vector_store.py` |
| Duplicate embedding model instantiation | `HuggingFaceEmbeddings(...)` was instantiated separately (and identically) in both `vector_store.py` and `qa_chain.py` instead of a shared source | Consolidated into `embeddings.py` |

## Open / Not Yet Fixed

| Issue | Description | Priority |
|---|---|---|
| Small effective context window | `flan-t5-base` has limited context; retrieved chunks are manually truncated to ~1200 characters, which can drop relevant content for complex questions | High — see ROADMAP.md |
| File-level citations only | Citations return the source filename, not the specific page/paragraph the answer came from | Medium |
| No conversation memory | Each question is answered independently; no multi-turn context | Medium |
| No automated tests | No unit tests for chunking, retrieval, or the `/ask` endpoint's response schema | Medium |
| No input validation on `/upload` | No check for empty files, oversized files, or corrupted PDFs before attempting to process them | Medium |
| No deployment | Runs locally only; no hosted version exists yet | High — blocks demoing to others without a screen-share |
| No rate limiting | `/ask` and `/upload` have no throttling; a script could spam requests | Low (not internet-facing yet) |
| CPU-only inference limits concurrency | Realistically supports only a handful of concurrent users (see ARCHITECTURE.md) | High — see ROADMAP.md |

## How to Add a New Issue
When you find a new bug or limitation, add a row to the "Open" table above with a short
description and a rough priority (High/Medium/Low), so this stays a live reference instead of
going stale.
