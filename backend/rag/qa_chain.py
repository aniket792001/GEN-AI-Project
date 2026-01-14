from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "faiss_index"


def truncate_docs(docs, max_chars=1200):
    context = ""
    for doc in docs:
        if len(context) >= max_chars:
            break
        context += doc.page_content + "\n"
    return context[:max_chars]


def get_rag_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=200,
        truncation=True,
        device=-1  # CPU
    )

    llm = HuggingFacePipeline(pipeline=pipe)

    prompt = PromptTemplate.from_template(
        """Answer the question using ONLY the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}

Answer:"""
    )

    def ask(question: str):
        # ✅ NEW LangChain API
        docs = retriever.invoke(question)

        # ✅ prevent token overflow
        context = truncate_docs(docs)

        answer = llm.invoke(
            prompt.format(context=context, question=question)
        )

        citations = list(
            {doc.metadata.get("source", "unknown") for doc in docs}
        )

        return {
            "answer": answer,
            "citations": citations
        }

    return ask
