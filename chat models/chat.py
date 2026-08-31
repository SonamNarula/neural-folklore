import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(dotenv_path=".env")

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("Missing GROQ_API_KEY in .env")

model = init_chat_model("groq:openai/gpt-oss-20b")
response = model.invoke(" tell me how to be accountable in my work and life")
print(response)