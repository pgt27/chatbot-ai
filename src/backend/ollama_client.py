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

env = os.environ.copy()
env["OLLAMA_HOST"] = "0.0.0.0"
env["OLLAMA_ORIGINS"] = "*"

def run_ollama_serve():
    subprocess.Popen(["ollama", "serve"], env=env)

thread = threading.Thread(target=run_ollama_serve)
thread.start()
time.sleep(5)  

def ensure_model_available(model: str) -> bool:
    try:
        tags = requests.get("http://localhost:11434/api/tags", timeout=5).json()
        if model in [m["name"] for m in tags.get("models", [])]:
            return True

        resp = requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model},
            stream=True,
            timeout=600
        )

        for line in resp.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode())

            if data.get("status") == "success":
                break

        tags = requests.get("http://localhost:11434/api/tags", timeout=5).json()
        return model in [m["name"] for m in tags.get("models", [])]

    except Exception as e:
        print("Lỗi ensure_model_available:", e)
        return False
        
PINGGY_URL = "http://tytji-34-124-205-38.a.free.pinggy.link"
DEFAULT_MODEL = "llama3.2:3b"
ensure_model_available(DEFAULT_MODEL)

def generate_response(prompt: str, model: str = DEFAULT_MODEL) -> str:
    try:
        url = f"{PINGGY_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            return response.json().get("response", "")
        return f"Lỗi API: {response.status_code}"

    except Exception as e:
        return f"Lỗi kết nối: {str(e)}"

def chat_with_history(messages: List[Dict[str, str]], model: str = "DEFAULT_MODEL) -> str:
    try:
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response["message"]["content"]

    except Exception:
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            ""
        )
        return generate_response(last_user_msg, model)






