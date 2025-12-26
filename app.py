import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# 1. Setup Page & API Key
st.set_page_config(page_title="Chat with Gemini", page_icon="🤖")
st.title("Gemini 2.5 Chat Assistant")


# You can also use os.getenv("GOOGLE_API_KEY") if using a .env file
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

if api_key:
    # 2. Initialize the Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite", 
        google_api_key= "AIzaSyCpceGVY5PTcT2d-bixK3F_lR8o85k3lS8",
        convert_system_message_to_human=True
    )

    # 3. Initialize Chat History in Session State
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm Gemini. How can I help you today?")
        ]

    # 4. Display Chat Messages
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    # 5. Handle User Input
    if user_query := st.chat_input("Type your message here..."):
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate response
        with st.chat_message("assistant"):
            # We pass the entire history so Gemini has context
            response = llm.invoke(st.session_state.chat_history)
            st.markdown(response.content)
            st.session_state.chat_history.append(AIMessage(content=response.content))
else:
    st.info("Please enter your Google API Key in the sidebar to start.")