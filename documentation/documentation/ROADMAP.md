# Roadmap

Ordered by priority — highest-impact, most interview-relevant items first.

## Phase 1: Core Quality (do next)
- [ ] Swap `flan-t5-base` (local CPU model) for a hosted LLM API (Gemini or OpenAI) to remove the
      context-window constraint and improve answer quality
- [ ] Add page-level citations (track page number during chunking, return it alongside filename)
- [ ] Add a small evaluation set (10-15 question/expected-answer pairs) to measure retrieval and
      answer quality, and use it to tune chunk size/overlap and `k` (number of retrieved chunks)
- [ ] Add basic unit tests (Pytest) for: chunking output, retrieval returning expected top-k
      results, and the `/ask` endpoint's response schema

## Phase 2: Production Readiness
- [ ] Deploy backend (Render/Railway) and frontend (Streamlit Community Cloud)
- [ ] Add input validation on `/upload` (file size limits, corrupted file handling)
- [ ] Add basic rate limiting on `/ask` and `/upload`
- [ ] Move secrets (API keys, once using a hosted LLM) to proper environment variable /
      secrets management instead of a local `.env` file only

## Phase 3: Feature Depth
- [ ] Add conversation memory for multi-turn follow-up questions
- [ ] Add hybrid search (keyword/BM25 + vector similarity) to catch exact-match queries
      (names, numbers, specific clauses) that pure semantic search can miss
- [ ] Support deleting/replacing a single uploaded document from the index without a full reset
- [ ] Move from local FAISS to a managed vector DB (Pinecone/Weaviate) for horizontal scaling

## Phase 4: Nice-to-Have
- [ ] Streaming responses in the Streamlit UI (typewriter effect, similar to the chatbot project)
- [ ] Multi-user support with isolated document collections per user
- [ ] Docker containerization for consistent deployment

## How to Use This Roadmap
Check items off as they're completed, and move fixed items into `KNOWN_ISSUES.md` under "Fixed"
with a short note on what changed. Re-prioritize phases if a specific interview or use case makes
one item more urgent than its current position.
