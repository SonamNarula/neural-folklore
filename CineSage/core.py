import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel


# Load API key
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")


# Model
model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)


# Schema
class Movie(BaseModel):
    title: str
    release_year: int
    genre: list[str]
    director: str
    cast: list[str]
    rating: float
    summary: str


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a professional Movie Information Extraction Assistant.

            Extract accurate information about the movie.

            Return:
            - title
            - release year
            - genre
            - director
            - main cast
            - rating
            - short summary

            Do not make up information.
            Keep the summary concise.
            """
        ),

        (
            "human",
            "Give me information about {movie_name}"
        )
    ]
)


# Structured output
structured_model = model.with_structured_output(Movie)


# Chain
chain = prompt | structured_model


# Function
def get_movie_info(movie_name):

    response = chain.invoke(
        {
            "movie_name": movie_name
        }
    )

    return response


# =========================================================
# TERMINAL
# =========================================================

if __name__ == "__main__":

    movie_name = input(
        "Give your movie name: "
    )

    result = get_movie_info(movie_name)

    print("\n")

    # Convert Pydantic object to JSON
    print(
        result.model_dump_json(
            indent=2
        )
    )