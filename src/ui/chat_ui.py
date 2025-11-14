import streamlit as st
import json
import datetime

def main():
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon="🤖",
        layout="centered"
    )
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""
    
    st.title("🤖 AI Chatbot")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Cài đặt")
        
        model_options = ["llama2", "mistral", "gemma"]
        selected_model = st.selectbox("Chọn model:", model_options)
        
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("💾 Lưu lịch sử"):
            save_chat_history()
        
        st.markdown("---")
        st.info("Chatbot Interface v1.0")
    
    display_chat_history()
    
    st.markdown("### Nhập tin nhắn:")
    user_input = st.text_area(
        "Nhập tin nhắn của bạn...",
        key="user_input",
        height=100,
        placeholder="Xin chào! Tôi có thể giúp gì cho bạn?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Gửi tin nhắn", use_container_width=True):
            if user_input.strip():
                process_user_message(user_input, selected_model)
                st.rerun()

def display_chat_history():
    """Hiển thị lịch sử chat"""
    if not st.session_state.chat_history:
        st.info("Chưa có tin nhắn nào. Hãy bắt đầu trò chuyện!")
        return
    
    chat_container = st.container()
    
    with chat_container:
        for i, chat in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(f"**Bạn:** {chat['user']}")
                st.caption(f"*{format_timestamp(chat['timestamp'])}*")
            
            with st.chat_message("assistant"):
                st.write(f"**AI:** {chat['ai']}")
                st.caption(f"*Model: {chat['model']} - {format_timestamp(chat['timestamp'])}*")
            
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("---")

def process_user_message(user_input, model):
    """Xử lý tin nhắn người dùng"""
    ai_response = generate_ai_response(user_input)
    
    st.session_state.chat_history.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user_input,
        "ai": ai_response,
        "model": model
    })
    
    st.session_state.user_input = ""

def generate_ai_response(user_input):
    """Tạo phản hồi AI giả lập"""
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ["xin chào", "hello", "hi"]):
        return "Xin chào! Tôi là AI chatbot. Tôi có thể giúp gì cho bạn?"
    elif any(word in user_input_lower for word in ["cảm ơn", "thanks"]):
        return "Không có gì! Rất vui được giúp đỡ bạn."
    elif any(word in user_input_lower for word in ["tạm biệt", "bye"]):
        return "Tạm biệt! Hẹn gặp lại bạn."
    else:
        return f"Tôi đã nhận được tin nhắn: '{user_input}'. Đây là phản hồi mẫu từ AI."

def save_chat_history():
    """Lưu lịch sử chat vào file JSON"""
    if st.session_state.chat_history:
        filename = f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(st.session_state.chat_history, f, ensure_ascii=False, indent=2)
            st.sidebar.success(f"Đã lưu vào {filename}")
        except Exception as e:
            st.sidebar.error(f"Lỗi khi lưu: {e}")
    else:
        st.sidebar.warning("Không có lịch sử chat để lưu")

def format_timestamp(timestamp_str):
    """Định dạng timestamp"""
    try:
        dt = datetime.datetime.fromisoformat(timestamp_str)
        return dt.strftime("%H:%M:%S %d/%m/%Y")
    except:
        return timestamp_str
