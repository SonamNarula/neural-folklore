import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env")

model = init_chat_model("google_genai:gemini-3.6-flash")
response = model.invoke("Hello! How are you today?")
print(response)