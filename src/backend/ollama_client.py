import streamlit as st
import os
import json
from typing import List, Dict, Any, Optional
import requests
import ollama
import threading
import time
import subprocess

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
    """Xóa toàn bộ lịch sử chat"""
    st.session_state.messages = [{"role": "ai", "content": "Có cần giúp gì hong?🥱"}]
    save_messages(st.session_state.messages)
    st.rerun()

def clear_history(filename: Optional[str] = None) -> None:
    path = history_path(filename)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

MODEL = "llama3.2:3b"
NGROK_URL = "https://phillis-jasperated-inexplicitly.ngrok-free.dev"
client = Client(host=NGROK_URL)
def ollama_chat(history_messages: List[Dict[str, str]]) -> str:
    response = client.chat(
        model=MODEL,
        messages=list(history_messages)
    )
    return response["message"]["content"]

