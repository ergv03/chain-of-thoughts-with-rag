from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st
import os

MODEL_TO_USE = "gpt-4"


def load_openai_api_key():
    """
    Load OpenAI API key into the environment
    """

    # Get openAI API Key from the form, and falls back to secrets. If secrets doesn't have a key, then an exception is raised
    openai_api_key_from_secrets = st.secrets.get('openai_credentials', {}).get('OPENAI_API_KEY')
    openai_api_key = st.session_state.get('openai_api_key') or openai_api_key_from_secrets

    if not openai_api_key:
        raise Exception('OPENAI API KEY is missing!')

    os.environ['OPENAI_API_KEY'] = openai_api_key


def query_chat_openai(system_message, user_message, model_to_use: str = MODEL_TO_USE, max_tokens: int = 1000):
    """
    Query OpenAI Chat API
    """

    chat = ChatOpenAI(temperature=0, model_name=model_to_use, max_tokens=max_tokens)

    message = [
        SystemMessage(
            content=system_message
        ),
        HumanMessage(
            content=user_message
        ),
    ]

    response = chat(message)

    return response.content
