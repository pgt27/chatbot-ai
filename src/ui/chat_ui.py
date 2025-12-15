import streamlit as st
import time
from src.backend.ollama_client import load_messages, save_messages, clear_chat
from src.backend.ollama_client import chat_with_history

def generate_ai_response(user_input: str) -> str:
    st.session_state.messages.append({"role": "user", "content": user_input})
    return chat_with_history(st.session_state.messages)

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
        
        /* KHUNG CHAT TRẮNG VỚI HEADER XANH Ở TRÊN */
        .stApp {{
            width: 400px;
            height: 680px;
            background: #ffffff;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
        <style>
        """,
        unsafe_allow_html=True
    )

def ui():
        # HEADER VỚI STREAMLIT COMPONENTS - CÓ THỂ TƯƠNG TÁC
    header_container = st.container()

    with header_container :
        b
        st.markdown("""
            < div style = "
            position: fixed;          /* Cố định */
        top: calc(50 % -340px);  /* Căn theo khung chat */
        left: 50 %;               /* Căn giữa ngang */
        transform: translateX(-50 %); /* Dịch về giữa */
        width: 400px;            /* ← THÊM: Cùng chiều rộng khung chat */
        background: #004aad;
        color: white;
        padding: 15px 20px;
        border - radius: 20px 20px 0 0;
        z - index: 100;           /* Tăng z-index */
        box - sizing: border - box;  /* Quan trọng: tính cả padding trong width */
        ">
        < div style = "display: flex; justify-content: space-between; align-items: center;" >
        <span style = "font-size: 1.2em; font-weight: bold;">
        Thanh niên nghiêm túc
        < / span>
        < / div>
        < / div>
        """, unsafe_allow_html=True)

        button_container = st.container()

    with button_container :
        st.markdown(
            
            """
            < style >
            /* Target the popover container */
            div[data - testid = "stPopover"] > div:first - child{
            background - color: #004aad !important; /* Blue background */
            border: 2px solid #004aad !important; /* Darker blue border */
            position: fixed;
            top: 10px;
            right: 20px;
            z - index: 200;
            border - radius: 10px !important; /* Rounded corners */
            color: white !important; /* White text color */
        }

        /* Target all text inside popover */
        div[data - testid = "stPopover"] > div:first - child* {
            color: white !important; /* Force white text for all elements */
        }

        /* Target buttons inside popover */
        div[data - testid = "stPopover"] button{
            background - color: rgba(0, 74, 173, 1) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }

        div[data - testid = "stPopover"] button:hover{
            background - color: rgba(255,255,255,0.2) !important;
        }
        < / style>
        """,
        unsafe_allow_html = True,
        )
    # NÚT 3 CHẤM DÙNG STREAMLIT POPOVER - CÓ THỂ TƯƠNG TÁC
  
        popover = st.popover("•••", help="Menu")
        
        with popover:        
            # NÚT XÓA CHAT - CÓ THỂ BẤM ĐƯỢC
            if st.button(
                "🗑️ Xóa đoạn chat",
                key="delete_chat_button",
                use_container_width=True,
                type="secondary"
            ):
                # Hiện xác nhận
                if st.session_state.get("confirm_delete", False):
                    clear_chat()
                    st.session_state.confirm_delete = False
                else:
                    st.session_state.confirm_delete = True
                    st.rerun()
            
            # Hiện thông báo xác nhận nếu cần
            if st.session_state.get("confirm_delete", False):
                st.warning("Bạn có chắc chắn muốn xóa?")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Có", use_container_width=True):
                        clear_chat()
                with col_no:
                    if st.button("❌ Không", use_container_width=True):
                        st.session_state.confirm_delete = False
                        st.rerun()
    
    # ========== CHAT CONTENT ==========
    st.markdown('<div class="chat-content">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    loaded = load_messages()
    if loaded:
        st.session_state["messages"] = loaded
    else:
        st.session_state["messages"] = [{"role": "assistant", "content": "Tôi cho phép em đặt câu hỏi 🥱"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== CHAT INPUT ==========
    f prompt := st.chat_input("Nhắn tin cho Thanh niên nghiêm túc ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_messages(st.session_state.messages)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thanh niên đang si nghĩ..."):
                ai_response = ollama_chat(st.session_state.messages)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                save_messages(st.session_state.messages)

def main_ui():
    apply_custom_styles()
    ui()





