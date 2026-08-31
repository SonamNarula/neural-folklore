import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("MISTRAL_API_KEY is missing from .env")

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)

response = model.invoke("Hello! How are you today?")

print(response.content)