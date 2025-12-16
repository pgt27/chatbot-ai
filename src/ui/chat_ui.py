import streamlit as st
import time
from src.backend.ollama_client import load_messages, save_messages, clear_chat
from src.backend.ollama_client import ollama_chat
from typing import List, Dict, Any, Optional

# HÀM MỚI: Khởi tạo session state
def initialize_session_state():
    """Khởi tạo tất cả session state - LUÔN VÀO chat_history_1.json ĐẦU TIÊN"""
    # DANH SÁCH CONVERSATIONS
    if "conversations" not in st.session_state:
        conversations = []
        
        # ===== LUÔN ƯU TIÊN chat_history_1.json ĐẦU TIÊN =====
        # 1. Thử load chat_history_1.json trước
        messages_1 = load_messages("chat_history_1.json")
        
        if messages_1:
            # Có file chat_history_1.json → tạo conversation 1
            conversations.append({
                "id": 1,
                "name": "Thanh niên nghiêm túc",
                "messages": messages_1,
                "active": True  # LUÔN ACTIVE KHI MỞ APP
            })
        else:
            # Không có file → tạo mới conversation 1
            conversations.append({
                "id": 1,
                "name": "Thanh niên nghiêm túc",
                "messages": [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}],
                "active": True  # LUÔN ACTIVE KHI MỞ APP
            })
            # Lưu file chat_history_1.json ngay
            save_messages(conversations[0]["messages"], "chat_history_1.json")
        
        # 2. Load các conversation khác (2, 3, ...) nếu có
        import os, glob
        from src.backend.ollama_client import history_path
        
        chat_files = glob.glob(history_path("chat_history_*.json"))
        for filepath in chat_files:
            filename = os.path.basename(filepath)
            # Bỏ qua chat_history_1.json (đã xử lý ở trên)
            if filename == "chat_history_1.json":
                continue
            
            try:
                # Lấy ID từ filename
                conv_id = int(filename.replace("chat_history_", "").replace(".json", ""))
                
                # Chỉ load nếu ID > 1
                if conv_id > 1:
                    messages = load_messages(filename)
                    if messages:
                        conversations.append({
                            "id": conv_id,
                            "name": f"Thanh niên nghiêm túc {conv_id}",
                            "messages": messages,
                            "active": False  # KHÔNG ACTIVE
                        })
            except:
                continue
        
        # Sắp xếp theo ID
        conversations.sort(key=lambda x: x["id"])
        
        st.session_state.conversations = conversations
        st.session_state.current_conversation_id = 1  # LUÔN LÀ 1
    
    # ID CHO CONVERSATION TIẾP THEO
    if "next_conversation_id" not in st.session_state:
        max_id = max([conv["id"] for conv in st.session_state.conversations]) if st.session_state.conversations else 0
        st.session_state.next_conversation_id = max_id + 1
    
    # CÁC STATE KHÁC
    if "show_conversation_list" not in st.session_state:
        st.session_state.show_conversation_list = False
    
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False
    
    if "delete_conv_id" not in st.session_state:
        st.session_state.delete_conv_id = None

# HÀM MỚI: Lưu conversation ra file riêng
def save_conversation_to_file(conversation_id: int, messages: List[Dict]):
    """Lưu tin nhắn của conversation ra file riêng"""
    filename = f"chat_history_{conversation_id}.json"
    save_messages(messages, filename)

# HÀM MỚI: Load conversation từ file
def load_conversation_from_file(conversation_id: int) -> List[Dict]:
    """Load tin nhắn của conversation từ file riêng"""
    filename = f"chat_history_{conversation_id}.json"
    return load_messages(filename)


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
        
        /* CSS cho tin nhắn */
        [data-testid="stChatMessageContent"] p {{
            color: black !important;
        }}
        
        div[data-testid="stChatMessage"][data-message-author="user"] 
        [data-testid="stChatMessageContent"] p {{
            color: #000000 !important;
            font-weight: 500;
        }}
        
        div[data-testid="stChatMessage"][data-message-author="assistant"] 
        [data-testid="stChatMessageContent"] p {{
            color: #333333 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # CSS cho màu chữ đen
    st.markdown(
        """
        <style> 
        .stChatMessage * {
            color: #000000 !important;
        }
        div[data-testid="stChatMessage"],
        div[data-testid="stChatMessage"] *,
        div[data-testid="stChatMessageContent"],
        div[data-testid="stChatMessageContent"] *,
        .stChatMessage p,
        .stChatMessage span,
        .stChatMessage div {
            color: #000000 !important;
        }
        .stSpinner,
        .stSpinner * {
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def ui():
    # KHỞI TẠO SESSION STATE TRƯỚC
    initialize_session_state()
    
    # TÌM CONVERSATION ĐANG ACTIVE VÀ LẤY MESSAGES CỦA NÓ
    current_messages = []
    for conv in st.session_state.conversations:
        if conv["active"]:
            current_messages = conv["messages"]
            break
    
    # NẾU KHÔNG TÌM THẤY, DÙNG MESSAGES MẶC ĐỊNH
    if not current_messages:
        current_messages = [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}]
    
    # ========== HEADER VỚI TÊN CONVERSATION HIỆN TẠI ==========
    header_container = st.container()
    
    with header_container:
        # Tìm conversation đang active
        current_conv_name = "Thanh niên nghiêm túc"
        for conv in st.session_state.conversations:
            if conv["active"]:
                current_conv_name = conv["name"]
                break
        
        st.markdown(f"""
        <div style="
            position: fixed;
            top: calc(50% - 340px);
            left: 50%;
            transform: translateX(-50%);
            width: 400px;
            background: #004aad;
            color: white;
            padding: 15px 20px;
            border-radius: 20px 20px 0 0;
            z-index: 100;
            box-sizing: border-box;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.2em; font-weight: bold;">
                    {current_conv_name}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ========== POPOVER MENU ==========
    button_container = st.container()

    with button_container:
        st.markdown(
        """
        <style>
        /* Target the popover container */
        div[data-testid="stPopover"] > div:first-child {
            background-color: #004aad !important;
            border: 2px solid #004aad !important;
            position: fixed; 
            top: 10px;
            right: 20px;
            z-index: 200;
            border-radius: 10px !important;
            color: white !important;
        }
        
        /* Target all text inside popover */
        div[data-testid="stPopover"] > div:first-child * {
            color: white !important;
        }
        
        /* Target buttons inside popover */
        div[data-testid="stPopover"] button {
            background-color: rgba(0, 74, 173, 1) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        
        div[data-testid="stPopover"] button:hover {
            background-color: rgba(255,255,255,0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        
        # NÚT 3 CHẤM DÙNG STREAMLIT POPOVER
        popover = st.popover("•••", help="Menu")
        
        with popover:
            # ========== XÓA ĐOẠN CHAT HIỆN TẠI ==========
            if st.button(
                "🗑️ Xóa đoạn chat",
                key="delete_chat_button",
                use_container_width=True,
                type="secondary"
            ):
                # Nếu đang hiện confirm, BẤM LẦN 2 SẼ TẮT
                if st.session_state.get("confirm_delete", False):
                    # BẤM LẦN 2: TẮT CONFIRM
                    st.session_state.confirm_delete = False
                else:
                    # BẤM LẦN 1: BẬT CONFIRM
                    st.session_state.confirm_delete = True
                st.rerun()
            
            # HIỆN THÔNG BÁO XÁC NHẬN NẾU confirm_delete = True
            if st.session_state.get("confirm_delete", False):
                st.warning("Bạn có chắc chắn muốn xóa?")
                
                # Cột CÓ - thực hiện xóa
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Có", use_container_width=True, key="confirm_yes"):
                        # GỌI HÀM XÓA
                        clear_chat()  # Hoặc clear_current_conversation()
                        # TẮT CONFIRM SAU KHI XÓA
                        st.session_state.confirm_delete = False
                        st.rerun()
                
                # Cột KHÔNG - hủy bỏ
                with col_no:
                    if st.button("❌ Không", use_container_width=True, key="confirm_no"):
                        # TẮT CONFIRM
                        st.session_state.confirm_delete = False
                        st.rerun()
            # ========== TẠO CUỘC HỘI THOẠI MỚI ==========
            if st.button(
                "➕ Tạo hội thoại mới",
                key="new_conversation_button",
                use_container_width=True,
                type="secondary"
            ):
                # TÌM ID TRỐNG NHỎ NHẤT (thay vì next_conversation_id)
                existing_ids = {conv["id"] for conv in st.session_state.conversations}
                
                # Tìm ID trống từ 2 trở lên (giữ conversation 1 cố định)
                new_id = 2
                while new_id in existing_ids:
                    new_id += 1
                
                new_name = f"Thanh niên nghiêm túc {new_id}"
                
                # Tắt active của tất cả conversations cũ
                for conv in st.session_state.conversations:
                    conv["active"] = False
                
                # Thêm conversation mới
                new_conversation = {
                    "id": new_id,
                    "name": new_name,
                    "messages": [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}],
                    "active": True
                }
                
                st.session_state.conversations.append(new_conversation)
                st.session_state.current_conversation_id = new_id
                
                # Lưu file mới
                save_conversation_to_file(new_id, new_conversation["messages"])
                
                st.toast(f"Đã tạo: {new_name} 🎉", icon="✅")
                st.rerun()
            
            # ========== DANH SÁCH ĐOẠN CHAT (TOGGLE) ==========
            if st.button(
                "📋 Danh sách đoạn chat",
                key="list_conversations_button", 
                use_container_width=True,
                type="secondary"
            ):
                # Toggle hiển thị danh sách
                st.session_state.show_conversation_list = not st.session_state.show_conversation_list
                st.rerun()
            
            # HIỂN THỊ DANH SÁCH CHUYỂN ĐẾN NẾU ĐANG BẬT
            if st.session_state.show_conversation_list:
                st.markdown("*Chuyển đến:*")
                
                for conv in st.session_state.conversations:
                    # Tạo row với 2 cột: nút chuyển và nút xóa
                    col_switch, col_delete = st.columns([4, 1])
                    
                    with col_switch:
                        # Nút chuyển đến conversation
                        if st.button(
                            f"{'🔵 ' if conv['active'] else '⚪ '}{conv['name']}",
                            key=f"switch_to_{conv['id']}",
                            use_container_width=True,
                            type="secondary" if not conv['active'] else "primary"
                        ):
                            # Tắt active của tất cả
                            for c in st.session_state.conversations:
                                c["active"] = False
                            
                            # Bật active cho conversation được chọn
                            conv["active"] = True
                            st.session_state.current_conversation_id = conv["id"]
                            st.session_state.messages = conv["messages"]
                            st.session_state.show_conversation_list = False
                            st.rerun()
                    
                    with col_delete:
                        # Nút xóa conversation - chỉ hiện nếu không phải conversation cuối cùng
                        if len(st.session_state.conversations) > 1:
                            if st.button(
                                "🗑️",
                                key=f"delete_conv_{conv['id']}",
                                help=f"Xóa {conv['name']}",
                                type="secondary"
                            ):
                                st.session_state.delete_conv_id = conv["id"]
                                st.rerun()
                        else:
                            st.empty()
                
                # XỬ LÝ XÓA CONVERSATION NẾU CÓ
                if st.session_state.delete_conv_id is not None:
                    conv_to_delete = None
                    for conv in st.session_state.conversations:
                        if conv["id"] == st.session_state.delete_conv_id:
                            conv_to_delete = conv
                            break
                    
                    if conv_to_delete:
                        st.divider()
                        st.warning(f"Xóa hoàn toàn '{conv_to_delete['name']}'?")
                        col_yes, col_no = st.columns(2)
                        
                        with col_yes:
                            if st.button("✅ Xóa vĩnh viễn", key="confirm_delete_conv", type="primary"):
                                # 1. Xóa conversation
                                st.session_state.conversations = [
                                    c for c in st.session_state.conversations 
                                    if c["id"] != st.session_state.delete_conv_id
                                ]
                                
                                # 2. Xóa file
                                import os
                                from src.backend.ollama_client import history_path
                                filename = f"chat_history_{st.session_state.delete_conv_id}.json"
                                filepath = history_path(filename)
                                if os.path.exists(filepath):
                                    os.remove(filepath)
                                
                                # 3. Nếu xóa conversation đang active
                                if conv_to_delete["active"] and st.session_state.conversations:
                                    st.session_state.conversations[0]["active"] = True
                                    st.session_state.current_conversation_id = st.session_state.conversations[0]["id"]
                                    st.session_state.messages = st.session_state.conversations[0]["messages"]
                                
                                # 4. KHÔNG CẦN CẬP NHẬT next_conversation_id nữa
                                # ID mới sẽ được tìm tự động
                                
                                st.session_state.delete_conv_id = None
                                st.toast(f"Đã xóa: {conv_to_delete['name']}", icon="🗑️")
                                st.rerun()
                        
                        with col_no:
                            if st.button(
                                "❌ Hủy bỏ", 
                                key="cancel_delete_conv",
                                use_container_width=True
                            ):
                                st.session_state.delete_conv_id = None
                                st.rerun()  

    # ========== CHAT CONTENT ==========
    st.markdown('<div class="chat-content">', unsafe_allow_html=True)
    
    # HIỂN THỊ MESSAGES CỦA CONVERSATION HIỆN TẠI
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== CHAT INPUT ==========
    if prompt := st.chat_input("Nhắn tin cho Thanh niên nghiêm túc ..."):
        # TÌM VÀ CẬP NHẬT CONVERSATION ĐANG ACTIVE
        active_conv = None
        for conv in st.session_state.conversations:
            if conv["active"]:
                active_conv = conv
                break
        
        if active_conv:
            # 1. THÊM USER MESSAGE VÀO CONVERSATION
            active_conv["messages"].append({"role": "user", "content": prompt})
            
            # 2. HIỂN THỊ USER MESSAGE
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 3. LẤY AI RESPONSE (dùng messages của conversation này)
            with st.chat_message("ai"):
                with st.spinner("Thanh niên đang si nghĩ..."):
                    ai_response = ollama_chat(active_conv["messages"])
                    st.markdown(ai_response)
            
            # 4. THÊM AI RESPONSE VÀO CONVERSATION
            active_conv["messages"].append({"role": "ai", "content": ai_response})
            
            # 5. LƯU CONVERSATION RA FILE RIÊNG
            save_conversation_to_file(active_conv["id"], active_conv["messages"])
            
            # 6. KHÔNG CẦN CẬP NHẬT st.session_state.messages
            st.rerun()

def main_ui():
    apply_custom_styles()
    ui()
