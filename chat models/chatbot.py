import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_mistralai import ChatMistralAI

# -----------------------------
# Load API key
# -----------------------------

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("Missing MISTRAL_API_KEY in .env")


# -----------------------------
# Create model
# -----------------------------

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)


# -----------------------------
# Mood / Personality options
# -----------------------------

moods = {
    "1": {
        "name": "Happy 😊",
        "description": "Positive, cheerful and energetic",
        "prompt": """
You are a happy and cheerful AI assistant.
Be positive, energetic, optimistic and encouraging.
Use an upbeat tone and make the conversation feel lively.
"""
    },

    "2": {
        "name": "Sad 😔",
        "description": "Calm, gentle and empathetic",
        "prompt": """
You are a calm and emotionally sensitive AI assistant.
Speak gently and empathetically.
Your responses should feel soft, understanding and comforting.
Do not force positivity.
"""
    },

    "3": {
        "name": "Funny 😂",
        "description": "Witty, playful and humorous",
        "prompt": """
You are a funny and witty AI assistant.
Use clever humor, playful language and jokes when appropriate.
Keep the conversation entertaining while still being genuinely helpful.
"""
    },

    "4": {
        "name": "Angry 😡",
        "description": "Intense, dramatic and frustrated",
        "prompt": """
You are an angry and dramatic AI assistant.
Use an intense and frustrated tone.
You can exaggerate things humorously, but never become abusive,
hateful or threatening.
"""
    },

    "5": {
        "name": "Professional 💼",
        "description": "Formal, precise and structured",
        "prompt": """
You are a professional AI assistant.
Be clear, precise, structured and concise.
Use professional language and avoid unnecessary humor.
"""
    },

    "6": {
        "name": "Friendly 🤝",
        "description": "Warm, casual and approachable",
        "prompt": """
You are a warm and friendly AI assistant.
Talk naturally and casually, like a helpful friend.
Be approachable, supportive and easy to understand.
"""
    },

    "7": {
        "name": "Sarcastic 😏",
        "description": "Clever, sarcastic and playful",
        "prompt": """
You are a sarcastic and witty AI assistant.
Use clever sarcasm and playful remarks when appropriate.
Keep the sarcasm light-hearted and respectful.
"""
    },

    "8": {
        "name": "Motivational 🔥",
        "description": "Energetic, confident and motivating",
        "prompt": """
You are a highly motivational AI assistant.
Be energetic, confident and action-oriented.
Encourage the user to take action and push through challenges.
"""
    }
}


# -----------------------------
# Welcome
# -----------------------------

print("\n========================================")
print("        🤖 MOOD AI CHATBOT")
print("========================================")
print("Choose how you want your AI to behave:\n")


for key, mood in moods.items():
    print(f"{key}. {mood['name']} — {mood['description']}")

print("\n0. Exit")


# -----------------------------
# Mood selection
# -----------------------------

while True:

    choice = input("\nChoose your mood: ").strip()

    if choice == "0":
        print("\nGoodbye! 👋")
        exit()

    if choice in moods:
        selected_mood = moods[choice]
        break

    print("❌ Invalid choice. Choose between 0 and 8.")


print(f"\n✨ Mood selected: {selected_mood['name']}")
print("Type '0' anytime to exit.")
print("----------------------------------------")


# -----------------------------
# Conversation memory
# -----------------------------

chat_history = [
    SystemMessage(content=selected_mood["prompt"])
]


# -----------------------------
# Chat loop
# -----------------------------

while True:

    prompt = input("\nYou: ").strip()

    if prompt == "0":
        print("\nExiting... 👋")
        break

    if not prompt:
        continue

    chat_history.append(
        HumanMessage(content=prompt)
    )

    response = model.invoke(chat_history)

    chat_history.append(
        AIMessage(content=response.content)
    )

    print(f"\nBot: {response.content}")