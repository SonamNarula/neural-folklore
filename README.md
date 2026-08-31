<div align="center">

# Neural Folklore

### Learning in public: Python + LLMs + AI engineering

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/Focus-LLMs%20%26%20AI%20Engineering-8A2BE2?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)

</div>

---

## About this repo

This repository is my learning journal for AI engineering, with a focus on:

- Python fundamentals
- LLM concepts and model behavior
- LangChain and AI app patterns
- API-based model access with Groq, Google, and Mistral
- hands-on experimentation and project building

This repo is intentionally practical and iterative. It is not a polished production app yet; it is a working archive of experiments, learning notes, and small AI projects.

---

## What has been done so far

The project setup is now in place and working at a basic level:

- created a Python virtual environment
- installed core dependencies from [requirements.txt](requirements.txt)
- configured local environment variables in a `.env` file
- tested LangChain chat model initialization
- verified a working Groq-based chat integration
- explored multiple model providers, including Groq, Google GenAI, and Mistral
- set up Git ignore rules to keep secrets out of version control

The working example currently uses Groq through LangChain and has been successfully validated with a real API key.

---

## Current repo structure

- [chat models/chat.py](chat%20models/chat.py) — current chat model example using LangChain
- [embedding models](embedding%20models) — work related to embeddings and vector workflows
- [requirements.txt](requirements.txt) — dependencies for the project
- [test.py](test.py) — scratch/test script
- [.gitignore](.gitignore) — ignores `.env`, virtual environments, and Python cache files

---

## Environment setup

From the project root:

```bash
cd "/Users/sonamnarula/Desktop/generative ai"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` file in the project root and add your keys there:

```env
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
```

> Keep your `.env` file local and never commit secrets to GitHub.

---

## Run the chat example

```bash
cd "/Users/sonamnarula/Desktop/generative ai"
source .venv/bin/activate
python "chat models/chat.py"
```

Current working pattern:

```python
model = init_chat_model("groq:openai/gpt-oss-20b")
response = model.invoke("Hello! How are you today?")
print(response)
```

This has been validated successfully.

---

## Provider exploration

The project has started testing multiple chat providers with LangChain:

- Groq
- Google Generative AI
- Mistral

This is useful for understanding provider differences, model naming conventions, and API setup patterns while building AI projects.

---

## Security note

API keys are treated as local secrets.

- do not commit `.env`
- do not upload raw credentials to GitHub
- keep secrets only in the local development environment
- rely on `.gitignore` to prevent accidental commits

---

## Next learning goals

1. build more structured AI mini-projects
2. explore embeddings and vector search
3. connect LLMs with tools and memory
4. build a small app using LangChain + local or remote models
5. document experiments and lessons as the repo grows

---

## Notes

This project is a record of learning by doing. The goal is progress, experimentation, and understanding how modern AI systems fit together in practice.

---

<div align="center">
<sub><i>Learning is the process. The repo is the trail.</i></sub>
</div>
