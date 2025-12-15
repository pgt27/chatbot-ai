
# HOW TO RUN CODE 
Step 1: Start Ollama Server
- Open First Command Prompt
set OLLAMA_HOST=0.0.0.0
set OLLAMA_ORIGINS=*
ollama serve

Step 2: Expose Ollama via Ngrok
- Open Second Command Prompt
winget install ngrok.ngrok
ngrok config add-authtoken 36svNXwUqRgPSBFTctAKaESpjns_dnDFEBPa8mibvBxKCWMV
ngrok http 11434

# Chatbot AI
![Grant Chatbot AI - Nhóm 4](./images/grantt.jpg)
