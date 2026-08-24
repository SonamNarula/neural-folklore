import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # .env file se variables load karta hai (jaise GROQ_API_KEY)

my_api_key = os.getenv("GROQ_API_KEY")  # .env se key nikalna

if not my_api_key:
    raise ValueError("GROQ_API_KEY is missing")  # agar key nahi mili to error

client = Groq(api_key=my_api_key)  # Groq se connect karne wala "client" object banaya

model = "llama-3.3-70b-versatile"  # kaunsa model use karna hai

prompt = "What is Machine Learning?"  # tera actual sawaal

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}]  # single user message bheja
)

answer = response.choices[0].message.content  # final answer nikalna
print(answer)