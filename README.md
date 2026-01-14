AI_Project/
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── rag/
│   │   ├── qa_chain.py         # RAG pipeline logic
│   │   ├── vector_store.py     # FAISS creation & loading
│
├── faiss_index/                # Saved FAISS vector database
├── data/                       # Uploaded / source documents
├── venv/                       # Virtual environment
├── requirements.txt
└── README.md



⚙️ Installation & Setup
1️⃣ Clone the repository

git clone https://github.com/your-username/rag-qa-system.git
cd rag-qa-system

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
B.Tech – Artificial Intelligence & Data Science
Aspiring AI / GenAI Engineer


⭐ Acknowledgements
LangChain
Hugging Face
FAISS
FastAPI
