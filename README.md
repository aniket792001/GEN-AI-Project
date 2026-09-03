GEN-AI-Project/
│
├── backend/
│   ├── main.py                  # FastAPI entry point (/upload, /ask, /reset)
│   └── rag/
│       ├── loader.py            # Document loading (PDF/DOCX/TXT)
│       ├── splitter.py          # Chunking logic
│       ├── embeddings.py        # Embedding model config
│       ├── vector_store.py      # FAISS creation, loading, reset
│       └── qa_chain.py          # RAG retrieval + generation pipeline
│
├── frontend/
│   └── app.py                   # Streamlit chat UI
│
├── tests/
│   ├── test_vector_store.py     # Tests for chunking/indexing logic
│   └── test_qa_chain.py         # Tests for the RAG ask() pipeline
│
├── documentation/
│   ├── ARCHITECTURE.md          # System design & data flow
│   ├── KNOWN_ISSUES.md          # Bug tracker (fixed + open)
│   ├── ROADMAP.md               # Planned improvements
│   └── SETUP.md                 # Local setup & troubleshooting
│
├── faiss_index/                 # Saved FAISS vector database (generated)
├── uploads/                     # Uploaded source documents (generated)
├── venv/                        # Virtual environment (not committed)
├── .env                         # API keys / secrets (not committed)
├── .gitignore
├── requirements.txt
└── README.md


⚙️ Installation & Setup
1️⃣ Clone the repository

git clone https://github.com/aniket792001/GEN-AI-Project.git
cd GEN-AI-Project

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Running the Application
Start the FastAPI server
uvicorn backend.main:app --reload


Server will start at:

http://127.0.0.1:8000

📬 API Endpoints
🔹 Ask a Question

POST /ask

Request Body

{
  "question": "What is deep learning?"
}


Response

{
  "answer": "Deep learning is a subset of machine learning that focuses on learning hierarchical representations using neural networks.",
  "citations": [
    "ml_notes.pdf"
  ]
}

🧠 How It Works (RAG Flow)
Documents are split into chunks
Chunks are embedded using Hugging Face embeddings
FAISS stores embeddings for fast similarity search
Relevant context is retrieved
LLM generates an answer only from retrieved context
Source citations are returned

⚠️ Known Limitations
Large context may be truncated (model max length = 512 tokens)
Answers depend on document quality
Uses CPU (slower than GPU)

📌 Future Improvements
🔄 Streaming responses
📄 Page-level citations
💬 Chat history & memory
🖥 Streamlit / React frontend
☁️ Deployment (Render / Railway)

👤 Author
Aniket Kadam
GenAI Engineer


⭐ Acknowledgements
LangChain
Hugging Face
FAISS
FastAPI
