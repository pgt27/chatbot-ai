# 🤖 Chatbot – Loading – Powered by Ollama LLM

> Đồ án môn học **Nhập môn Công nghệ Thông tin** > **Khoa Công nghệ Thông tin > Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM**

Dự án này xây dựng một Chatbot AI có giao diện trực quan, hỗ trợ đa cuộc hội thoại, lưu trữ lịch sử và kết nối với mô hình ngôn ngữ lớn thông qua Ollama Server.

---

## 🤖 Giao diện (UI)
<img src="./images/ui.jpg" width="1734" height="1079" />

# How to run 
1) Upload the file 2A_ollama_pinggy_ngrok.ipynb to Google Colab and run cells. (change !ollama pull gpt-oss:20b  -->   !ollama pull llama3.2:1b)
2) Create a Colab Secret with: (Name: NGROK_API_KEY / Value: your Ngrok API key.) 
3) After the notebook finishes running, locate the line: * ngrok tunnel https://......ngrok-free.dev -> http://127.0.0.1:11434
4) Copy the Ngrok URL (e.g. https://......ngrok-free.dev) and assign it to NGROK_URL = "...."
5) Run the application code to start the chatbot.
   
---
## Cấu trúc thư mục

```
chatbot-/
├── images/                                 # Hình ảnh minh họa
│   ├── grantt.jpg                          # Giản đồ grantt 
│   └── ui.jpg                              # Giao diện game
│   
├── src/                                    # Source code
│   ├── backend/                            
│   │   └── ollama_client.py                # Các hàm quản lý bộ nhớ hội thoại và kết nối Ollama API              
│   └── ui/ 
│       └── chat_ui.py                      # Tạo giao diện chatbot, xử lý nhập/xuất và quản lý đa cuộc hội thoại
├── 2A_ollama_pinggy_ngrok.ipynb            # Dùng chạy Ollama Server trên Google Colab và public API qua tunnel (Ngrok)
├── main.py                                 # Điểm khởi chạy chính của chương trình 
├── requirements.txt                        # Danh sách thư viện cần thiết
└── README.md                               # Tài liệu hướng dẫn và mô tả project
```

---

## Tác giả:

### Loading Chatbot - 25CTT3

| Thành viên | MSSV |
| :--- | :--- |
| Phạm Gia | 25120233 |
| Nguyễn Đình Thi | 25120231 |
| Huỳnh Hoàng Nguyên | 25120213 |
| Lương Hoàng Phúc | 25120221 |
| Nguyễn Trần Hùng Sơn | 25120228 |

Giảng viên hướng dẫn thực hành: Thầy Lê Đức Khoan.

---

<img src="./images/grantt.jpg" width="1734" height="1079" />

---
