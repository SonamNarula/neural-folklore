import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY .env file me nahi mili bhai")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"
role = "user"
prompt = "Do you know Padho with Pratyush"

message = {
    "role": role,
    "content": prompt,
}

messages = [message]

try:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
except Exception as error:
    print("Groq API call fail ho gayi.")
    print("Check karo:")
    print("1. .env me GROQ_API_KEY valid hai")
    print("2. internet connection chal raha hai")
    print("3. Groq dashboard me key active hai")
    print(f"Actual error: {error}")
    raise

print("#######################################")

answer = response.choices[0].message.content
print(answer)
