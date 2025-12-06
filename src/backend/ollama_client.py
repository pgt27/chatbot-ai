import os
import json
from typing import List, Dict, Any, Optional


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


def clear_history(filename: Optional[str] = None) -> None:
    path = history_path(filename)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def generate_response_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]
        )
        return response['message']['content']
    except Exception as e:
        try:
            url = "http://localhost:11434/api/generate"
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Lỗi kết nối Ollama: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "Không thể kết nối đến Ollama. Hãy chắc chắn rằng Ollama đang chạy (chạy lệnh 'ollama serve')"
        except Exception as e2:
            return f"Lỗi: {str(e2)}"

def generate_response_with_history(messages: List[Dict[str, str]], model: str = "llama3.2:3b") -> str:
    try:
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        response = ollama.chat(
            model=model,
            messages=formatted_messages
        )
        return response['message']['content']
    except Exception as e:
        if messages:
            last_user_message = next((msg['content'] for msg in reversed(messages) if msg['role'] == 'user'), None)
            if last_user_message:
                return generate_response_ollama(last_user_message, model)
        return "Xin lỗi, đã có lỗi xảy ra khi kết nối với AI."

