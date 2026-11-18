# 🔍 Autonomous Research Agent

An AI agent that researches any topic autonomously using a ReAct loop — searches the web, reads full articles, and writes a structured markdown report.

## Live Demo
👉 https://week3-research-agent-8emjp7vdstwehamuqi4soc.streamlit.app/

## How it works
1. User enters a research topic
2. Agent searches the web using Tavily
3. Agent reads full pages for deeper information
4. Agent writes a complete structured report
5. Report saved as markdown file

## Stack
- **LangGraph** — ReAct agent loop
- **Groq** — LLM inference (qwen/qwen3.8-27b)
- **Tavily** — web search and URL extraction
- **Streamlit** — frontend UI
- **Python** — backend

## Architecture

User Input → ReAct Loop → web_search / read_url → Final Report


## Setup
```bash
git clone https://github.com/omshrirao-dev/week3-research-agent
cd week3-research-agent
pip install -r requirements.txt
```
Create `.env`:

TAVILY_API_KEY=your_key
GROQ_API_KEY=your_key

```bash
streamlit run app.py
<<<<<<< HEAD
```
=======
```
>>>>>>> 8a8adb962df08c4c5a4cb8e888e8f301e4e516f6
