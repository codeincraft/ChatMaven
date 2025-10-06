import streamlit as st
from streamlit_chat import message as st_message
import os
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage)


st.set_page_config(
    page_title="Chat with AI",
    page_icon="🌍"
)

# Custom wrapper for messages
def bot_message(text, key=None):
    st_message(text, key=key,
               avatar_style="bottts", seed="ChatMaven")

def user_message(text, key=None):
    st_message(text, is_user=True, key=key, avatar_style="personas", 
               seed="User1001")

def init():
    # Use Streamlit secrets for API key (works both locally and on cloud)
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        os.environ["OPENAI_API_KEY"] = api_key
        return True
    except Exception as e:
        st.error("OPENAI_API_KEY is not set in secrets")
        return False
    
def main():
    if not init():
        st.stop()
    
    chat = ChatOpenAI(temperature=0.2)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are ChatMaven, an AI assistant that helps people find information."),
        ]
    
    st.header("ChatMaven 🌍")

    # Display chat history (skip SystemMessage at index 0)
    for i, msg in enumerate(st.session_state.messages[1:]):
        if isinstance(msg, HumanMessage):
            user_message(msg.content, key=f"{i}_user")
        elif isinstance(msg, AIMessage):
            bot_message(msg.content, key=f"{i}_ai")

    with st.sidebar:
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Your message:", key="user_input")
            send_button = st.form_submit_button("Send")
        
        if send_button and user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("ChatMaven is thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            st.rerun()

if __name__ == "__main__":
    main()
