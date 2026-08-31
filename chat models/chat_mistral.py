import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv(dotenv_path=".env")

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("Missing MISTRAL_API_KEY in .env")

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)

response = model.invoke("Hello! How are you today?")
print(response)