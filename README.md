# 🤖 RAG Agent — AI-Powered Knowledge Assistant

A fully functional AI agent that can search documents, browse the web, perform calculations, and send WhatsApp messages — all from a simple web interface.

---

## 🚀 Features

- 📄 **PDF Upload & Q&A** — Upload any PDF and ask questions about it
- 🔍 **Hybrid Document Search** — BM25 + Semantic search for accurate retrieval
- 🌐 **Web Search** — DuckDuckGo + Tavily fallback for real-time information
- 🧮 **Calculator** — Handles math expressions automatically
- 💬 **WhatsApp Automation** — Send messages via natural language commands
- 🧠 **Conversation Memory** — Remembers previous messages in a session
- ⚡ **Fast API Backend** — Built with FastAPI, served via Uvicorn

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (llama-3.3-70b-versatile) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| Retrieval | LangChain + BM25 Hybrid Search |
| Backend | FastAPI |
| Browser Automation | Playwright |
| Frontend | HTML + JavaScript |

---

## 📁 Project Structure

```
RAG_Agent/
├── rag.py                  # Document loading, chunking, ChromaDB, hybrid search
├── agents.py               # LangChain agent with tools
├── Fastapi.py              # FastAPI backend
├── state.py                # Shared state for PDF upload
├── index.html              # Frontend UI
├── data.txt                # Company knowledge base
├── whatsapp_automation/
│   └── open_whatsapp.py    # WhatsApp automation
├── .env                    # API keys (not committed)
└── requirements.txt
```

---

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/kanhaiya-ML/Projects.git
cd Projects
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file**
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get free API keys:
- Groq → https://console.groq.com
- Tavily → https://app.tavily.com

**4. Run the API**
```bash
uvicorn Fastapi:app --reload
```

**5. Open `index.html` in browser**

---

## 💡 How to Use

**Ask questions from company documents:**
```
"What is the return policy?"
"How long does delivery take?"
```

**Upload PDF and ask questions:**
- Click Upload PDF → select file → ask questions about it

**Web search:**
```
"What is the latest news in AI today?"
"Current iPhone 15 price in India?"
```

**Math:**
```
"What is 25% of 3500?"
```

**WhatsApp:**
```
"Send WhatsApp message to Rahul saying Hello"
```

---

## 🔑 Agent Tools

| Tool | Description |
|---|---|
| `DocsSearch` | Searches uploaded documents using hybrid RAG |
| `WebSearch` | Searches internet using DuckDuckGo + Tavily |
| `Calculator` | Evaluates math expressions |
| `WhatsAppMessage` | Sends WhatsApp messages via Playwright |

---

## 📊 Architecture

```
User Query
    ↓
FastAPI Backend
    ↓
LangChain Agent (Groq LLM)
    ↓
┌─────────────────────────────┐
│ Tool Selection               │
├──────────────┬──────────────┤
│ DocsSearch   │ WebSearch    │
│ Calculator   │ WhatsApp     │
└──────────────┴──────────────┘
    ↓
Response → Frontend
```

---

## 🙋 About

Built by **Kanhaiya**.

- GitHub: [@kanhaiya-ML](https://github.com/kanhaiya-ML)
- No college degree. Just consistency. 💪
