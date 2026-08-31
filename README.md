<div align="center">

# Neural Folklore

### Learning in public: Python + LLMs + AI engineering

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/Focus-LLMs%20%26%20AI%20Engineering-8A2BE2?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)
![Stack](https://img.shields.io/badge/Stack-LangChain%20%7C%20Groq%20%7C%20HuggingFace-1f2937?style=for-the-badge)

</div>

---

## Overview

Neural Folklore is a personal AI engineering learning repo built around experimentation, documentation, and rapid iteration.

The focus is to understand how modern AI systems work in practice:

- Python fundamentals and clean scripting
- LLM behavior and prompting
- LangChain-based app patterns
- hosted AI APIs and model access
- embeddings and vector workflows
- local open-source models via Hugging Face

This is not a polished production app. It is a living knowledge base and working playground for AI learning.

---

## What I’ve built so far

The repo now includes a basic but working AI stack setup:

- Python environment configured and running
- LangChain installed and tested
- chat model integration working with Groq
- experimentation across Groq, Google GenAI, and Mistral
- embedding generation tested with hosted providers and local Hugging Face models
- a working Mistral-powered chatbot prototype built in [chat models/chatbot.py](chat%20models/chatbot.py)
- project structure organized around learning modules and experiments

This is the foundation for moving from “learning AI” to “building with AI.”

---

## Project structure

- [chat models/chat.py](chat%20models/chat.py) — LangChain chat model setup
- [chat models/chatbot.py](chat%20models/chatbot.py) — interactive chatbot using Mistral
- [embedding models/embeddings.py](embedding%20models/embeddings.py) — API-based embedding examples
- [embedding models/huggingface_embeddings.py](embedding%20models/huggingface_embeddings.py) — local Hugging Face embedding example
- [requirements.txt](requirements.txt) — Python dependencies
- [test.py](test.py) — scratch/testing script
- [.gitignore](.gitignore) — excludes local secrets and environment files

---

## Current stack

- Python
- LangChain
- Groq
- Google Generative AI
- Mistral
- Hugging Face sentence-transformers
- dotenv for local environment configuration

---

## Setup

From the project root:

```bash
cd "/Users/sonamnarula/Desktop/generative ai"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` file and add your keys:

```env
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
```

> Keep secrets local. Never commit `.env` or API keys to GitHub.

---

## Run the chat examples

### Basic model test

```bash
cd "/Users/sonamnarula/Desktop/generative ai"
source .venv/bin/activate
python "chat models/chat.py"
```

Working pattern:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:openai/gpt-oss-20b")
response = model.invoke("Hello! How are you today?")
print(response)
```

### Interactive chatbot

```bash
cd "/Users/sonamnarula/Desktop/generative ai"
source .venv/bin/activate
python "chat models/chatbot.py"
```

This chatbot uses Mistral through LangChain and keeps taking user prompts until you enter `0` to exit.

---

## Embedding experiments

The repo includes both hosted and local embedding approaches.

### Hosted embeddings

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vector = embeddings.embed_query("You are going to learn Gen AI")
print(vector)
```

### Local embeddings with Hugging Face

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = ["Hello world", "Bonjour le monde"]
print(embeddings.embed_documents(texts))
```

These examples help compare managed APIs against local open-source embedding workflows.

---

## Learning roadmap

1. Python and problem solving
2. LLM fundamentals and prompting
3. LangChain app patterns
4. model provider integration and API setup
5. embeddings and retrieval concepts
6. build small end-to-end AI tools and demos

---

## Security note

This project follows a simple rule:

- no secrets in git history
- no raw API keys in the repo
- keep credentials only in a local `.env` file
- use `.gitignore` to avoid accidental exposure

---

## Closing note

This repository is a trail of learning: experiments, wins, mistakes, and the steady path from curiosity to capability.

The goal is not perfection. The goal is momentum.

---

<div align="center">
<sub><i>Learning is the process. The repo is the trail.</i></sub>
</div>
