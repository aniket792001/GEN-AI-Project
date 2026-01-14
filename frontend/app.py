import streamlit as st
import requests

# ----------------------------
# Config
# ----------------------------
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Document Q&A Assistant",
    layout="centered"
)

# ----------------------------
# Session State
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# UI Header
# ----------------------------
st.title("📄 Document Q&A Assistant")
st.caption("Ask questions strictly based on uploaded documents")

st.divider()

# ----------------------------
# Upload Section
# ----------------------------
st.subheader("📤 Upload Document")

uploaded_file = st.file_uploader(
    "Supported formats: PDF, DOCX, TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    if st.button("Upload & Index"):
        with st.spinner("Uploading and indexing document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={"file": uploaded_file},
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Document indexed successfully!")
                    st.json(data)
                else:
                    st.error("❌ Upload failed")

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

# ----------------------------
# Chat Section
# ----------------------------
st.subheader("💬 Ask a Question")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": question},
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": data["answer"],
                            "citations": data["citations"]
                        }
                    )
                else:
                    st.error("Failed to get answer")

            except Exception as e:
                st.error(f"Error: {e}")

# ----------------------------
# Display Chat History
# ----------------------------
if st.session_state.chat_history:
    st.divider()
    st.subheader("📜 Chat History")

    for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{i}:** {chat['question']}")
        st.markdown(f"**Answer:** {chat['answer']}")

        if chat["citations"]:
            with st.expander("📌 Citations"):
                for c in chat["citations"]:
                    st.json(c)

        st.markdown("---")

# ----------------------------
# Controls
# ----------------------------
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.success("Chat cleared")

with col2:
    if st.button("🔄 Reset Knowledge Base"):
        try:
            response = requests.post(f"{BACKEND_URL}/reset")
            if response.status_code == 200:
                st.success("Vector store reset successfully")
            else:
                st.error("Failed to reset vector store")
        except Exception as e:
            st.error(f"Error: {e}")
