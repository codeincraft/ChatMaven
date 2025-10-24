import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from streamlit_chat import message as st_message
import os
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage)


st.set_page_config(
    page_title="Chat with AI",
    page_icon="🌍",
    layout="wide"
)

# Modern CSS with integrated send button
st.markdown("""
<style>
    /* Sticky container for cloud compatibility */
    [data-testid="stForm"] {
        position: sticky;
        bottom: 0;
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-top: 1px solid #3a3a3a;
        z-index: 999;
    }
    
    /* Ensure proper spacing */
    .main .block-container {
        padding-bottom: 2rem;
    }
    
    /* Container for input wrapper */
    [data-testid="stForm"] > div {
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Style the textarea container */
    .stTextArea {
        position: relative;
    }
    
    /* Modern dark textarea styling */
    .stTextArea textarea {
        background-color: #2d2d2d !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 24px !important;
        color: #e0e0e0 !important;
        padding: 14px 60px 14px 20px !important;
        font-size: 15px !important;
        resize: none !important;
        min-height: 52px !important;
        max-height: 200px !important;
        line-height: 1.5 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #555 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #888 !important;
    }
    
    /* Position send button inside textarea */
    [data-testid="stForm"] [data-testid="column"]:last-child {
        position: absolute;
        right: 8px;
        bottom: 8px;
        width: auto !important;
        z-index: 10;
    }
    
    /* Style the send button */
    .stButton button {
        background-color: #404040 !important;
        color: #e0e0e0 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 36px !important;
        height: 36px !important;
        padding: 0 !important;
        min-height: 36px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton button:hover {
        background-color: #505050 !important;
    }
    
    .stButton button:active {
        background-color: #606060 !important;
    }
    
    /* Hide button text, show only emoji */
    .stButton button p {
        font-size: 18px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }
    
    /* Make first column take full width */
    [data-testid="stForm"] [data-testid="column"]:first-child {
        width: 100% !important;
        position: relative;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        [data-testid="stForm"] {
            padding: 1rem;
        }
        
        .stTextArea textarea {
            font-size: 14px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Custom wrapper for messages
def bot_message(text, key=None):
    st_message(text, key=key,
               avatar_style="bottts", seed="ChatMaven")

def user_message(text, key=None):
    st_message(text, is_user=True, key=key, avatar_style="personas", 
               seed="User1001")

def init():
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
    st.markdown("---")

    # Display chat history
    for i, msg in enumerate(st.session_state.messages[1:]):
        if isinstance(msg, HumanMessage):
            user_message(msg.content, key=f"{i}_user")
        elif isinstance(msg, AIMessage):
            bot_message(msg.content, key=f"{i}_ai")
    
    # Modern input field with integrated send button
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 0.001])
        
        with col1:
            user_input = st.text_area(
                "Message", 
                key="user_input",
                placeholder="Ask anything",
                label_visibility="collapsed",
                height=52,
                max_chars=None
            )
        
        with col2:
            send_button = st.form_submit_button("↑", use_container_width=False)
    
    # Only process when send button is clicked
    if send_button and user_input and user_input.strip():
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatMaven is thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        st.rerun()

if __name__ == "__main__":
    main()
