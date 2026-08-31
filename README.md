<div align="center">

# Neural Folklore

### Learning in public: Python + LLMs + AI engineering

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/Focus-LLMs%20%26%20AI%20Engineering-8A2BE2?style=for-the-badge)
![Status](https://img.shields.io/badge/status-learning-brightgreen?style=for-the-badge)

</div>

---

## About this repo

This repository is a personal learning journal focused on Python, LLMs, and AI engineering.

The goal is to explore the practical side of AI development through:

- Python and software fundamentals
- prompt engineering and model behavior
- LangChain workflows
- API-based LLM integrations
- small experiments and prototypes

This is a working repo, not a polished product.

---

## Current project setup

The example chat script in [chat models/chat.py](chat%20models/chat.py) is currently configured to use Groq via LangChain.

### Required setup

1. Create a local [.env](.env) file in the project root.
2. Add your Groq key:

```env
GROQ_API_KEY=your_key_here
```

3. Never commit the `.env` file or any API secrets to Git.

---

## Repo structure

- [chat models/chat.py](chat%20models/chat.py) — LangChain chat model example using Groq
- [embedding models](embedding%20models) — embeddings experiments and related work
- [requirements.txt](requirements.txt) — Python dependencies
- [test.py](test.py) — scratch/test script

---

## Quick start

```bash
git clone https://github.com/SonamNarula/neural-folklore.git
cd neural-folklore
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create your local `.env` file with the Groq key before running the chat example:

```bash
python "chat models/chat.py"
```

---

## Working example

The current working approach uses Groq with a valid model such as:

```python
model = init_chat_model("groq:openai/gpt-oss-20b")
```

This has been verified to work with a valid Groq API key.

---

## Security note

Keep all API keys local.

- Do not commit [.env](.env)
- Do not push raw secrets to GitHub
- Add `.env` and similar secret files to `.gitignore`

This repo is meant to document the learning journey, not expose credentials.

---

## Notes

This project is structured around curiosity, iteration, and learning by building.

---

<div align="center">
<sub><i>Learning is the process. The repo is the trail.</i></sub>
</div>
