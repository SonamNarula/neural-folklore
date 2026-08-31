from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = ["Hello world", "Bonjour le monde"]

vectors = embeddings.embed_documents(texts)

print(vectors)