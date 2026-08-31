import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mistralai import ChatMistralAI

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("Missing MISTRAL_API_KEY in .env")

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)

chat_history = []

while True:
    print("-----------------------------welcome to the chatbot-----------------------------")

    prompt = input("You: ")

    if prompt == "0":
        print("Exiting...")
        break

    chat_history.append(
        HumanMessage(content=prompt)
    )

    response = model.invoke(chat_history)

    chat_history.append(
        AIMessage(content=response.content)
    )

    print("Bot:", response.content)