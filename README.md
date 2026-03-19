# SHREY DeepSearch Agent 🚀

**SHREY DeepSearch Agent** is a proprietary, autonomous multi-agent research engine designed for high-fidelity financial analysis and deep investigative research. Powered by **Llama-3.3-70B** and real-time web evidence, it replicates the "Deep Research Mode" of advanced AI assistants with a focus on investment-grade accuracy and transparency.

Designed and Developed by: **Shreyans Jain**

---

## ✨ Key Features

- **Autonomous Agentic Planning**: Dynamically decomposes complex queries (e.g., *"Analyze the impact of AI on Indian IT margins until 2027"*) into multi-step investigative roadmaps.
- **Multi-Modal Live Research**: Performs real-time web searches across News and Web domains using DuckDuckGo, ensuring results are up-to-the-minute.
- **Ultra-Robust Scraping**: Uses a multi-layered extraction strategy (Trafilatura + BeautifulSoup recovery) with browser emulation to bypass bot protection on premium research sites.
- **Verbose Thought Logging**: Features a real-time "Mission Control" log that exposes the agent's reasoning, search queries, and scraping status as they happen.
- **Evidence-First Synthesis**: Generates professional reports where every insight is linked directly to its source URL for instant verification.
- **Instant PDF Export**: High-fidelity PDF generation of research findings directly from the dashboard.
- **KPI Extraction Engine**: Automatically identifies and structures hard financial metrics (CAGR, EBITDA, Market Cap) from messy web data into consolidated tables.

---

## 🛠️ Technology Stack

- **Large Language Model**: [Groq](https://groq.com/) (Llama-3.3-70B-Versatile)
- **Backend Framework**: FastAPI (Asynchronous SSE Streaming)
- **Search Engine**: DuckDuckGo DDGS (Autonomous querying)
- **Scraping Portfolio**: Trafilatura, BeautifulSoup4, Requests
- **Frontend**: Vanilla JS, CSS3 (Glassmorphism), Marked.js (Markdown rendering)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com/keys) (Free tier available)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Shreyyyyy/deepsearch-agent.git
cd deepsearch-agent

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_actual_api_key_here
```
*(Note: `.env` is git-ignored for security. Do not commit your secrets!)*

### 4. Run the Agent
```bash
python server.py
```
Visit `http://localhost:8000` to initiate your first research mission.

---

## 🏗️ Architecture Overview

The SHREY engine operates in five distinct phases:
1. **Query Deconstruction**: Llama-3 analyzes intent, sector, and depth requirements.
2. **Dynamic Planning**: The `ResearchPlanner` constructs a tailored investigation roadmap.
3. **Evidence Loop**: The `ResearchExecutor` autonomously searches, scrapes, and performs micro-analysis on web sources.
4. **Metric Synthesis**: The `FinancialAnalysisModule` aggregates statistics and KPIs found in the Evidence Loop.
5. **Narrative Synthesis**: The `ReportGenerator` weaves everything into a cohesive, evidence-backed final report.

---

## 📄 License

Proprietary Research Tool. Designed for professional and educational use.

---
Created with ❤️ by **Shreyans Jain**
