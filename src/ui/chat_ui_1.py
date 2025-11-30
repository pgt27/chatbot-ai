import streamlit as st
import time
from src.backend.ollama_client import load_messages, save_messages

def generate_ai_response(user_input):
    time.sleep(0.5)
    return f"Thanh niên : '{user_input}'"

def apply_custom_styles():
    st.markdown(
        f"""
        <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(to right, #000000, #3533cd);
            height: 100vh;
            display: grid;
            place-items: center;
        }}
        header {{ 
            visibility: hidden; 
        }}
        .block-container {{ 
            padding-top: 0rem; padding-bottom: 0rem; 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def ui():
    st.markdown(
        f"""
        <style>
        .stApp {{
            width: 400px;
            height: 680px;
            background: #ffffff;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
        </style>
        <div style = "background: #004aad; color: white; padding: 10px 15px; border-radius: 30px 30px;">
            <div style = "display: flex; justify-content: space-between; align-items: center;">
                <span style = "font-size: 1.2em; font-weight: bold;">
                    Thanh niên nghiêm túc
                </span> 
                <div>
                    <span style = "margin-right: 15px; cursor: pointer;">
                        &#8226; &#8226; &#8226;
                    </span>
                    <span style = "cursor: pointer;"> 
                        &#x2715; 
                    </span> 
                </div>
            </div>  
        </div>
        """,
        unsafe_allow_html=True
    )
    if "messages" not in st.session_state:
        loaded = load_messages()
        if loaded:
            st.session_state["messages"] = loaded
        else:
            st.session_state["messages"] = [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Nhắn tin cho Thanh niên nghiêm túc ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_messages(st.session_state.messages)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("ai"):
            with st.spinner("Thanh niên đang si nghĩ..."):
                ai_response = generate_ai_response(prompt)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "ai", "content": ai_response})
                save_messages(st.session_state.messages)
def main_ui():
    apply_custom_styles()
    ui()

