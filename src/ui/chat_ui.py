
import streamlit as st
import time

PRIMARY_COLOR = "#004aad"  
SECONDARY_COLOR = "#F0F0FF" 
BACKGROUND_COLOR = "#FFF" 
BORDER_COLOR = "#E0BBE4"    

def generate_ai_response(user_input):
    """Giả lập phản hồi từ AI."""
    time.sleep(0.5)
    return f"Công chúa: '{user_input}'"

def apply_custom_styles():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BACKGROUND_COLOR};
            max-width: 400px; 
            margin: auto;
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15); 
            border: 1px solid {BORDER_COLOR}; 
            overflow: hidden; 
        }}

       
        header {{ visibility: hidden; }}
        .block-container {{ padding-top: 0rem; padding-bottom: 0rem; }}
        
        
        .st-emotion-cache-r423a6 {{ 
            background-image: linear-gradient(to right, #000000, #3533cd); 
            color: white;
            padding: 15px 15px 15px 20px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            margin-top: 0px !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }}
        
        .stChatMessage {{
            border-radius: 12px;
            padding: 5px 10px;
            margin-bottom: 10px;
        }}

        .stChatMessage:nth-child(odd) {{ 
            background-color: {SECONDARY_COLOR}; 
            color: #333333;
        }}
        
        .stChatMessage:nth-child(even) {{ 
            background-color: #F0FFF0; 
            color: #333333;
        }}

        div[data-testid="stChatInput"] {{
            border-top: 1px solid {BORDER_COLOR};
            padding: 10px 15px;
            background-color: #FFFFFF;
        }}
        
        div[data-testid="stChatInput"] label {{ display: none; }}
        div[data-testid="stChatInput"] svg {{ visibility: hidden; }}
        
        
        button[data-testid="baseButton"] {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 50%; 
            width: 35px;
            height: 35px;
            line-height: 0;
            margin-left: 5px;
        }}
        button[data-testid="baseButton"]:hover {{
            background-color: #E63999; 
        }}
        
        input[type="text"] {{
            border-radius: 20px;
            border: 1px solid {BORDER_COLOR};
            padding: 10px 15px;
            font-style: italic;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


def main_ui():
    apply_custom_styles()
    
    st.markdown(
        f"""
        <div style="background-image: linear-gradient(to right, #FF33CC, #CC33FF); color: white; padding: 10px 15px; border-top-left-radius: 15px; border-top-right-radius: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.2em; font-weight: bold;">Chat with us</span>
                <div>
                    <span style="margin-right: 15px; cursor: pointer;">&#8226;&#8226;&#8226;</span> 
                    <span style="cursor: pointer;">&#x2715;</span> </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
   
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "ai", "content": "Chào bé, chị có thể giúp gì cho bé hong?"}]

   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

   
    if prompt := st.chat_input("Type a message..."):
        
       
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

       
        with st.chat_message("ai"):
            with st.spinner("Công chúa đang si nghĩ..."):
                ai_response = generate_ai_response(prompt)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "ai", "content": ai_response})

if __name__ == "__main__":
    main_ui()
