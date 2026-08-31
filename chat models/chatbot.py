import os

from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain_mistralai import ChatMistralAI


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("Missing MISTRAL_API_KEY in .env")


# =========================================================
# CREATE MODEL
# =========================================================

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)


# =========================================================
# MOODS
# =========================================================

moods = {

    "1": {
        "name": "Angry 😡",
        "description": "Intense, dramatic and frustrated",

        "prompt": """
You are an angry and dramatic AI assistant.

Use an intense and frustrated tone.

You can exaggerate things humorously.

However, never become abusive, hateful or threatening.

Still provide useful and accurate answers.
"""
    },


    "2": {
        "name": "Funny 😂",
        "description": "Witty, playful and humorous",

        "prompt": """
You are a funny and witty AI assistant.

Use clever humor, playful language and jokes
when appropriate.

Keep the conversation entertaining while still
being genuinely helpful.

Do not make every response a joke.
"""
    },


    "3": {
        "name": "Sad 😔",
        "description": "Calm, gentle and empathetic",

        "prompt": """
You are a calm and emotionally sensitive AI assistant.

Speak gently and empathetically.

Your responses should feel soft, understanding
and comforting.

Do not force positivity.
"""
    },


    "4": {
        "name": "Happy 😊",
        "description": "Positive, cheerful and energetic",

        "prompt": """
You are a happy and cheerful AI assistant.

Be positive, energetic, optimistic and encouraging.

Use an upbeat tone and make the conversation
feel lively.

Still provide accurate and useful answers.
"""
    },


    "5": {
        "name": "Professional 💼",
        "description": "Formal, precise and structured",

        "prompt": """
You are a professional AI assistant.

Be clear, precise, structured and concise.

Use professional language.

Avoid unnecessary humor and keep your answers
focused and useful.
"""
    },


    "6": {
        "name": "Friendly 🤝",
        "description": "Warm, casual and approachable",

        "prompt": """
You are a warm and friendly AI assistant.

Talk naturally and casually like a helpful friend.

Be approachable, supportive and easy to understand.

Keep the conversation comfortable and natural.
"""
    },


    "7": {
        "name": "Sarcastic 😏",
        "description": "Clever, sarcastic and playful",

        "prompt": """
You are a sarcastic and witty AI assistant.

Use clever sarcasm and playful remarks when
appropriate.

Keep the sarcasm light-hearted and respectful.

Do not let sarcasm reduce the usefulness
or accuracy of your answers.
"""
    },


    "8": {
        "name": "Motivational 🔥",
        "description": "Energetic, confident and motivating",

        "prompt": """
You are a highly motivational AI assistant.

Be energetic, confident and action-oriented.

Encourage the user to take action.

Push the user to keep improving and not give up.

Give practical advice along with motivation.
"""
    }
}


# =========================================================
# WELCOME
# =========================================================

print("\n========================================")
print("        🤖 MOOD AI CHATBOT")
print("========================================")

print("\nChoose your AI mode:\n")

print("Press 1 for Angry Mode 😡")
print("Press 2 for Funny Mode 😂")
print("Press 3 for Sad Mode 😔")
print("Press 4 for Happy Mode 😊")
print("Press 5 for Professional Mode 💼")
print("Press 6 for Friendly Mode 🤝")
print("Press 7 for Sarcastic Mode 😏")
print("Press 8 for Motivational Mode 🔥")
print("Press 0 to Exit")


# =========================================================
# MOOD SELECTION
# =========================================================

while True:

    choice = input("\nEnter your choice: ").strip()

    if choice == "0":
        print("\nGoodbye! 👋")
        exit()

    if choice in moods:

        selected_mood = moods[choice]

        print(
            f"\n✨ {selected_mood['name']} activated!"
        )

        print(
            selected_mood["description"]
        )

        print(
            "\nType '0' anytime to exit."
        )

        print("----------------------------------------")

        break

    print(
        "❌ Invalid choice. "
        "Please enter a number from 0 to 8."
    )


# =========================================================
# CHAT HISTORY
# =========================================================

chat_history = [

    SystemMessage(
        content=selected_mood["prompt"]
    )

]


# =========================================================
# CHAT LOOP
# =========================================================

while True:

    prompt = input("\nYou: ").strip()


    # -------------------------
    # Exit
    # -------------------------

    if prompt == "0":

        print("\nExiting... 👋")

        break


    # -------------------------
    # Empty input
    # -------------------------

    if not prompt:

        print("Please enter something.")

        continue


    # -------------------------
    # Add user message
    # -------------------------

    chat_history.append(

        HumanMessage(
            content=prompt
        )

    )


    # -------------------------
    # Get AI response
    # -------------------------

    try:

        response = model.invoke(
            chat_history
        )


        # -------------------------
        # Save AI response
        # -------------------------

        chat_history.append(

            AIMessage(
                content=response.content
            )

        )


        # -------------------------
        # Display response
        # -------------------------

        print(
            f"\nBot [{selected_mood['name']}]: "
            f"{response.content}"
        )


    except Exception as e:

        print(
            f"\n❌ Something went wrong: {e}"
        )