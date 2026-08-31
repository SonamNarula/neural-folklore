import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("Missing MISTRAL_API_KEY in .env")

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)

while True :
    print("-----------------------------welcome to the chatbot-----------------------------")
    prompt = input("You: ")

    if prompt == "0":
        print("Exiting...")
        break

    response = model.invoke(prompt)

    print("Bot:", response.content)