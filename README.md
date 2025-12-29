# AI Engineering Bootcamp 🚀

A documented 30-day accelerated journey from Legacy Systems/IT to Modern AI Engineering. This repository contains progressive labs focusing on **Generative AI**, **Agents**, and **RAG (Retrieval-Augmented Generation)**.

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **LLM:** Google Gemini 2.5 Flash / Lite
- **Orchestration:** LangChain & LangGraph
- **Vector DB:** ChromaDB (Local Persistent Storage)
- **Frontend:** Streamlit

## 📂 Key Projects

### 🤖 1. Corporate Policy AI Assistant (Day 13)
*A RAG-based chatbot that answers questions about internal documents using Metadata filtering.*
- **Features:** "Ask your PDF" functionality, Department-specific filtering (Metadata), Streamlit UI.
- [View Code](./day13_app.py)

### 🕵️ 2. Autonomous SysAdmin Agent (Day 9)
*An intelligent agent capable of using custom tools to diagnose server health.*
- **Features:** Tool calling, Reasoning/ReAct pattern, LangGraph state machine.
- [View Code](./day9_agent.py)

## ⚡ How to Run
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/trentdouthat/ai-engineering-bootcamp.git](https://github.com/trentdouthat/ai-engineering-bootcamp.git)
   cd ai-engineering-bootcamp

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Configure Environment:**
    Create a .env file in the root directory:
    Properties
    GOOGLE_API_KEY=your_key_here
    GEMINI_MODEL=gemini-2.5-flash-lite

4. **Run the App:**
    ```bash
    streamlit run day13_app.py