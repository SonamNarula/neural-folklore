import os
import streamlit as st

from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain_mistralai import ChatMistralAI


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MoodAI",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
}

.stApp {
    background:
        radial-gradient(circle at 15% -10%, rgba(139,92,246,0.18), transparent 45%),
        radial-gradient(circle at 90% 10%, rgba(56,189,248,0.10), transparent 40%),
        linear-gradient(135deg, #060810 0%, #0d1220 45%, #080b14 100%);
}

#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

.block-container {
    max-width: 850px;
    padding-top: 2.5rem;
}


/* Main title */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 2px;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #a78bfa, #8b5cf6, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 18px rgba(139,92,246,0.35));
}

.subtitle {
    text-align: center;
    color: #6b7891;
    font-size: 0.85rem;
    letter-spacing: 1px;
    margin-bottom: 30px;
}


/* Section label */

h3 {
    color: #cbd5e1 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px;
}


/* Selectbox */

[data-baseweb="select"] > div {
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(139, 92, 246, 0.35) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
}
[data-baseweb="select"] div, [data-baseweb="select"] span {
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
ul[role="listbox"] {
    background: #0d1220 !important;
    border: 1px solid rgba(139, 92, 246, 0.35) !important;
}


/* Mood card */

.mood-card {
    padding: 22px 24px;
    border-radius: 18px;
    background: linear-gradient(160deg, rgba(30,41,59,0.75), rgba(15,20,32,0.75));
    border: 1px solid var(--mood-color, rgba(139, 92, 246, 0.35));
    border-left: 4px solid var(--mood-color, #8b5cf6);
    box-shadow: 0 0 24px -8px var(--mood-color, rgba(139,92,246,0.5));
    margin-bottom: 22px;
    margin-top: 14px;
    transition: all 0.3s ease;
}

.mood-label {
    color: #6b7891;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 700;
}

.mood-name {
    color: white;
    font-size: 1.5rem;
    font-weight: 800;
    margin-top: 6px;
}

.mood-description {
    color: #94a3b8;
    margin-top: 6px;
    font-size: 0.9rem;
}


/* Chat messages */

[data-testid="stChatMessage"] {
    background: rgba(20, 26, 41, 0.75);
    border: 1px solid #263247;
    border-radius: 16px;
    margin-bottom: 12px;
    padding: 4px 6px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
}

[data-testid="stChatMessage"] p {
    color: #dbe4f0;
    line-height: 1.6;
    font-size: 0.94rem;
}


/* Input */

[data-testid="stChatInput"] {
    border-top: 1px solid #1c2333;
    padding-top: 14px;
}

[data-testid="stChatInput"] textarea {
    background: #0d1220 !important;
    color: white !important;
    border: 1px solid #2d3548 !important;
    border-radius: 14px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 1px #8b5cf6, 0 0 20px -4px rgba(139,92,246,0.6) !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #8b5cf6, #38bdf8) !important;
    border-radius: 10px !important;
}


/* Button */

.stButton button {
    width: 100%;
    border-radius: 12px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid #374151;
    color: #cbd5e1;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.2s ease;
}
.stButton button:hover {
    border-color: #8b5cf6;
    color: white;
    box-shadow: 0 0 16px -4px rgba(139,92,246,0.7);
}


/* Scrollbar */

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #060810; }
::-webkit-scrollbar-thumb { background: #2d3548; border-radius: 4px; }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD ENV
# =========================================================

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    st.error("❌ Missing MISTRAL_API_KEY in .env")
    st.stop()


# =========================================================
# MODEL
# =========================================================

model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)


# =========================================================
# MOODS
# =========================================================

MOODS = {

    "Happy 😊": {
        "description": "Positive, cheerful and energetic",
        "color": "#facc15",

        "prompt": """
You are a happy and cheerful AI assistant.

Be positive, energetic, optimistic and encouraging.

Use an upbeat and lively tone.

Still give accurate and useful answers.
"""
    },

    "Sad 😔": {
        "description": "Calm, gentle and empathetic",
        "color": "#60a5fa",

        "prompt": """
You are a calm and empathetic AI assistant.

Speak gently and thoughtfully.

Be understanding and emotionally sensitive.

Do not force positivity.
"""
    },

    "Funny 😂": {
        "description": "Witty, playful and humorous",
        "color": "#fb923c",

        "prompt": """
You are a funny and witty AI assistant.

Use clever humor, playful language and jokes when appropriate.

Keep the conversation entertaining while remaining helpful.
"""
    },

    "Angry 😡": {
        "description": "Dramatic, intense and frustrated",
        "color": "#f87171",

        "prompt": """
You are an angry and dramatic AI assistant.

Use an intense and frustrated tone.

You may exaggerate things humorously.

Never become abusive, hateful or threatening.
"""
    },

    "Professional 💼": {
        "description": "Formal, precise and structured",
        "color": "#94a3b8",

        "prompt": """
You are a professional AI assistant.

Be clear, precise, structured and concise.

Use professional language.

Avoid unnecessary humor.
"""
    },

    "Friendly 🤝": {
        "description": "Warm, casual and approachable",
        "color": "#4ade80",

        "prompt": """
You are a warm and friendly AI assistant.

Talk naturally and casually like a helpful friend.

Be approachable, supportive and easy to understand.
"""
    },

    "Sarcastic 😏": {
        "description": "Clever, sarcastic and playful",
        "color": "#f472b6",

        "prompt": """
You are a sarcastic and witty AI assistant.

Use clever sarcasm and playful remarks when appropriate.

Keep the sarcasm light-hearted and respectful.
"""
    },

    "Motivational 🔥": {
        "description": "Confident, energetic and motivating",
        "color": "#a78bfa",

        "prompt": """
You are a highly motivational AI assistant.

Be energetic, confident and action-oriented.

Encourage the user to take action.

Push them to keep improving and not give up.
"""
    }
}


# =========================================================
# SESSION STATE
# =========================================================

if "mood" not in st.session_state:

    st.session_state.mood = "Funny 😂"


if "chat_history" not in st.session_state:

    st.session_state.chat_history = [
        SystemMessage(
            content=MOODS[
                st.session_state.mood
            ]["prompt"]
        )
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 MoodAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'YOUR AI · YOUR PERSONALITY · YOUR MOOD'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# MOOD SELECTION
# =========================================================

st.subheader("🎭 Choose your AI personality")


selected_mood = st.selectbox(
    "How should your AI behave?",
    list(MOODS.keys()),
    index=list(MOODS.keys()).index(
        st.session_state.mood
    ),
    label_visibility="collapsed"
)


# =========================================================
# MOOD CHANGE
# =========================================================

if selected_mood != st.session_state.mood:

    st.session_state.mood = selected_mood

    st.session_state.chat_history = [
        SystemMessage(
            content=MOODS[selected_mood]["prompt"]
        )
    ]

    st.rerun()


# =========================================================
# CURRENT MOOD CARD
# =========================================================

current_color = MOODS[st.session_state.mood]["color"]

st.markdown(
    f"""
    <div class="mood-card" style="--mood-color: {current_color};">

        <div class="mood-label">
            CURRENT PERSONALITY
        </div>

        <div class="mood-name">
            {st.session_state.mood}
        </div>

        <div class="mood-description">
            {MOODS[st.session_state.mood]["description"]}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# RESET CHAT
# =========================================================

if st.button("🗑️ Start New Conversation"):

    st.session_state.chat_history = [
        SystemMessage(
            content=MOODS[
                st.session_state.mood
            ]["prompt"]
        )
    ]

    st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.chat_history:

    if isinstance(message, HumanMessage):

        with st.chat_message(
            "user",
            avatar="🧑‍💻"
        ):
            st.markdown(message.content)


    elif isinstance(message, AIMessage):

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):
            st.markdown(message.content)


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    f"Talk to your {st.session_state.mood} AI..."
)


# =========================================================
# CHAT RESPONSE
# =========================================================

if prompt:

    # Add user message

    st.session_state.chat_history.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message(
        "user",
        avatar="🧑‍💻"
    ):

        st.markdown(prompt)


    # Generate response

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.chat_history
            )

            st.markdown(
                response.content
            )


    # Save response

    st.session_state.chat_history.append(
        AIMessage(
            content=response.content
        )
    )