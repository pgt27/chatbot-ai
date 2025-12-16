import streamlit as st
import os
import json
from typing import List, Dict, Any, Optional
import requests
from ollama import Client
from collections import deque


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def history_path(filename: Optional[str] = None) -> str:
    fname = filename or "chat_history.json"
    return os.path.join(_project_root(), fname)

def load_messages(filename: Optional[str] = None) -> List[Dict[str, Any]]:
    path = history_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        return []
    return []


def save_messages(messages: List[Dict[str, Any]], filename: Optional[str] = None) -> None:
    path = history_path(filename)
    tmp = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass


def clear_chat():
    """Xóa toàn bộ lịch sử chat của conversation hiện tại"""
    # TÌM CONVERSATION ĐANG ACTIVE TRONG SESSION STATE
    if hasattr(st, 'session_state') and 'conversations' in st.session_state:
        for conv in st.session_state.conversations:
            if conv.get("active"):
                # RESET MESSAGES CỦA CONVERSATION NÀY
                conv["messages"] = [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}]
                
                # LƯU RA FILE RIÊNG
                filename = f"chat_history_{conv['id']}.json"
                save_messages(conv["messages"], filename)
                
                # CẬP NHẬT session_state.messages (để tương thích code cũ)
                st.session_state.messages = conv["messages"]
                break
    else:
        # FALLBACK: DÙNG LOGIC CŨ
        st.session_state.messages = [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}]
        save_messages(st.session_state.messages)
    
    st.rerun()

def get_conversation_filename(conversation_id: int) -> str:
    """Tạo filename cho conversation"""
    return f"chat_history_{conversation_id}.json"

def save_conversation_to_file(conversation_id: int, messages: List[Dict]):
    """Lưu/ghi đè tin nhắn của conversation ra file riêng"""
    filename = f"chat_history_{conversation_id}.json"
    save_messages(messages, filename)  # Hàm này đã có ghi đè file cũ

def load_conversation_messages(conversation_id: int) -> List[Dict[str, Any]]:
    """Load messages của conversation cụ thể"""
    filename = get_conversation_filename(conversation_id)
    return load_messages(filename)

MODEL = "llama3.2:1b"
NGROK_URL = "https://phillis-jasperated-inexplicitly.ngrok-free.dev/"
client = Client(host=NGROK_URL)
def ollama_chat(history_messages: List[Dict[str, str]]) -> str:
    response = client.chat(
        model=MODEL,
        messages=list(history_messages)
    )
    return response["message"]["content"]
