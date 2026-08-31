<div align="center">

# 🧠 Neural Folklore

### *"this is me trying"*

**A final-year CSE student's public build log — moving from Software Engineering into AI Engineering, one committed lesson at a time.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Status](https://img.shields.io/badge/status-actively%20building-brightgreen?style=for-the-badge)
![Open to Work](https://img.shields.io/badge/open%20to-SDE%20%2F%20AI%20Engineering%20roles-important?style=for-the-badge)

[Notes](#-llm-engineering-notes) · [What Works Today](#-what-actually-works-today) · [Repo Map](#-repo-map) · [Setup](#-getting-started) · [Progress](#-progress-snapshot) · [Connect](#-lets-connect)

</div>

---

## 👋 About

I'm Sonam — a final-year CSE student navigating placement season while deliberately building toward **AI Engineering**: building *with* foundation models (LLMs, RAG, agentic systems) rather than training them from scratch.

> **Background:** a competitive-programming foundation first — 500+ LeetCode problems, Knight tier, AtCoder Brown — now redirected at Python fluency, LLM tooling, and production-shaped AI systems.

I'm learning Python properly first (it demands a different daily-driver fluency than CP ever did), while running a parallel, from-scratch curriculum on how LLMs actually work — and shipping small, working things along the way instead of just collecting notes.

This repo is that trail: less "polished portfolio," more **working in the open** — what's learned, what's built, and what's still queued, tracked honestly rather than dressed up.

---

## ✅ What actually works today

Not just notes — code that runs:

- 🔌 **Multi-provider LLM integration** via LangChain — [Groq](<chat models/chat_groq.py>), [Gemini](<chat models/chat_gemini.py>), [Mistral](<chat models/chat_mistral.py>), and HuggingFace (both [hosted endpoint](<chat models/huggingface.py>) and [local pipeline](<chat models/localmodel.py>))
- 🤖 A working **terminal chatbot** with rolling conversation memory, powered by Mistral — [`chatbot.py`](<chat models/chatbot.py>)
- 🧬 **Embedding pipelines**, both hosted ([Google/Mistral](<embedding models/embeddings.py>)) and fully local ([sentence-transformers](<embedding models/huggingface_embeddings.py>)) — for comparing managed APIs against open-source alternatives
- 📚 A **6-part, written-from-scratch LLM engineering curriculum** — tokenization and attention through agents, tools, and memory — kept current with where the field stood as of writing (MoE architectures, reasoning models, local inference)
- 🐍 **Python fundamentals, tracked lesson-by-lesson**, with mini-projects that only get built *after* the matching lesson is actually done — never before

---

## 🗺️ Repo map

```
neural-folklore/
├── LLMs/                 → 6-part deep-dive LLM engineering curriculum
├── PYTHON/                → fundamentals & control-flow lessons (live tracker inside)
├── PYTHON PROJECTS/       → mini-projects applying those lessons (live tracker inside)
├── chat models/           → multi-provider LangChain chat integrations
├── embedding models/      → hosted + local embedding experiments
├── requirements.txt       → full AI/ML dependency stack
└── pyproject.toml         → project metadata (uv-managed)
```

Two of these folders keep their own detailed, self-updating trackers — worth a look:
- [`PYTHON/readme.md`](<PYTHON/readme.md>) — lesson-by-lesson checklist across 9 modules (fundamentals → control flow → OOP → GUI)
- [`PYTHON PROJECTS/README.md`](<PYTHON%20PROJECTS/README.md>) — a 20-project build queue, each unlocked only once its prerequisite lessons are done

---

## 📖 LLM Engineering Notes

Written as a personal, from-scratch curriculum — not copied from a single course. Each note pairs a Hinglish explanation with a clean English summary, because being able to explain a concept simply is as much the point as understanding it.

| Day | Topic | What it covers |
|:---:|-------|-----------------|
| 1 | [**LLM Basics**](<LLMs/Day 1 BASICS.md>) | Tokenization, attention, how prediction actually happens — plus 2026-era context: MoE architectures, reasoning/thinking models, long context windows |
| 2 | [**Hugging Face**](<LLMs/Day 2 HUGGING FACE.md>) | Where open-source models live, quantization, and what will actually run on modest hardware |
| 3 | [**Ollama + LM Studio**](<LLMs/Day%203%20Ollama%20+%20LM%20Studio.md>) | Running quantized LLMs locally — no cloud bill, no API key |
| 4 | [**Prompting**](<LLMs/Day 4 Prompting.md>) | Prompt engineering fundamentals, and how reasoning models are reshaping which techniques still matter |
| 5 | [**LangChain Basics**](<LLMs/Day 5 LangChain Basics.md>) | Chains vs. agents, LCEL, and using an LLM as one component inside a larger system |
| 6 | [**Tools, Memory & Agents**](<LLMs/Day%206%20Tool%20%2C%20Memory%20and%20Agent.md>) | Giving an agent reach beyond its own knowledge (tools) and continuity across turns (memory) — closes with a working Q&A bot |

---

## 📊 Progress snapshot

Tracked honestly — nothing here is marked done until the file exists and runs.

| Track | Status |
|-------|--------|
| Python — Fundamentals | ![8/8](https://img.shields.io/badge/8%2F8-complete-brightgreen?style=flat-square) |
| Python — Control Flow | ![3/8](https://img.shields.io/badge/3%2F8-in%20progress-yellow?style=flat-square) |
| Applied mini-projects | ![4/20](https://img.shields.io/badge/4%2F20-building-orange?style=flat-square) |
| LLM engineering curriculum | ![6 days](https://img.shields.io/badge/6%20days-written-8A2BE2?style=flat-square) |
| Multi-provider chat integration | ![working](https://img.shields.io/badge/Groq%20%7C%20Gemini%20%7C%20Mistral%20%7C%20HF-working-brightgreen?style=flat-square) |
| Embeddings (hosted + local) | ![working](https://img.shields.io/badge/hosted%20%2B%20local-working-brightgreen?style=flat-square) |

---

## 🧰 Tech stack

**Core**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white)

**LLM orchestration**
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square)

**Model providers**
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square)
![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat-square&logo=googlegemini&logoColor=white)
![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=flat-square)
![HuggingFace](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

**Embeddings & vector stores**
![Sentence Transformers](https://img.shields.io/badge/sentence--transformers-FFD21E?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-6C3EF4?style=flat-square)
![Pinecone](https://img.shields.io/badge/Pinecone-1B1B1F?style=flat-square)

**Serving / tooling**
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)

---

## 🚀 Getting started

```bash
git clone https://github.com/SonamNarula/neural-folklore.git
cd neural-folklore

python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Create a local `.env` in the project root and add whichever keys you plan to use:

```env
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
```

> `.env` is git-ignored by default. Never commit real keys.

**Try a chat model:**

```bash
python "chat models/chat_groq.py"
```

**Talk to the memory-backed chatbot:**

```bash
python "chat models/chatbot.py"
# keeps chatting until you type 0 to exit
```

**Run an embedding experiment:**

```bash
python "embedding models/embeddings.py"            # hosted (Google / Mistral)
python "embedding models/huggingface_embeddings.py" # fully local
```

---

## 🧭 Roadmap

**Python:** While Loops → For Loops → Collections → Functions → OOP → Files & Exceptions → Concurrency & APIs → PyQt5 GUI apps — each unlocking the next batch of mini-projects.

**AI Engineering:** wire up a retrieval pipeline over FAISS/Chroma, build a first real RAG project end-to-end, extend the Day 6 agent into something tool-rich and deployable, and serve a demo via FastAPI or Streamlit.

---

## 🔒 A quiet engineering habit

- No secrets in git history, ever
- No raw API keys committed — `.env` only, always git-ignored
- Nothing is marked "done" in a tracker until its file exists and actually runs

Small habits, but the kind that are supposed to carry over into anything shipped later.

---

## 📫 Let's connect

![GitHub](https://img.shields.io/badge/GitHub-SonamNarula-181717?style=for-the-badge&logo=github&logoColor=white)
![Email](https://img.shields.io/badge/Email-sonamnarula2108%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)

If you're hiring for SDE or AI Engineering roles, or just want to talk shop about LLMs — my inbox is open.

---

<div align="center">

*"and I'm never gonna stop being scared of storms, but I'm always gonna be here doing the work anyway."*

<sub><i>Learning is the process. The repo is the trail.</i></sub>

</div>
