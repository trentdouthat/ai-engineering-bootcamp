AI Engineering Bootcamp 🚀
A documented 30-day accelerated journey from Legacy Systems/IT to Modern AI Engineering. This repository contains progressive labs focusing on Generative AI, Agents, and RAG (Retrieval-Augmented Generation).
🛠️ Tech Stack
Language: Python 3.12+
LLM: Google Gemini 2.5 Flash / Lite
Orchestration: LangChain & LangGraph
Vector DB: ChromaDB (Local Persistent Storage)
Frontend: Streamlit
📂 Key Projects
👁️ 1. OpsVision Pro (Day 23)
A RAG-based inventory scanner that identifies hardware and retrieves manuals.
Features: Visual Object Detection, Vector Search, PDF Spec Retrieval.
View Code | Live Demo
🎥 2. Recall Video Search (Day 26)
A "Ctrl+F" engine for video content.
Features: Automated JSON timeline generation, Chat-with-Video interface.
View Code
🎙️ 3. SRVA Voice Agent (Day 29)
A hands-free Site Reliability Engineer assistant.
Features: Voice-to-Voice interface, Autonomous Tool Calling (LangGraph), System Health Monitoring.
View Code
📈 Learning Timeline
[x] Week 1: LLM Fundamentals & Prompt Engineering
[x] Week 2: RAG Pipelines, Vector Databases, and Agents
[x] Week 3: Computer Vision, Speech Processing, & Video Intelligence
[x] Week 4: Full Stack Deployment & Portfolio Construction
⚡ How to Run
Clone the repo:
git clone [https://github.com/trentdouthat/ai-engineering-bootcamp.git](https://github.com/trentdouthat/ai-engineering-bootcamp.git)
cd ai-engineering-bootcamp


Install dependencies:
pip install -r requirements.txt


Configure Environment:
Create a .env file in the root directory:
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite


Run the App:
streamlit run day23_opsvision.py


