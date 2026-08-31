import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

text = "You are going to learn Gen AI"

if os.getenv("GOOGLE_API_KEY"):
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector = embeddings.embed_query(text)
    print("Using Google embeddings")
elif os.getenv("MISTRAL_API_KEY"):
    from langchain_mistralai import MistralAIEmbeddings

    embeddings = MistralAIEmbeddings(model="mistral-embed")
    vector = embeddings.embed_query(text)
    print("Using Mistral embeddings")
else:
    print("No embedding API key found. Add GOOGLE_API_KEY or MISTRAL_API_KEY in your local .env file.")
    raise SystemExit(1)

print(vector)
print(f"Embedding length: {len(vector)}")