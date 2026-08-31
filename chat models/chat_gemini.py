import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env")

model = init_chat_model("google_genai:gemini-3.6-flash", api_key=api_key)
response = model.invoke("write a poem on ai")

if isinstance(response.content, str):
    print(response.content)
else:
    for block in response.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block.get("text", ""))