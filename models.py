"""
Model initialization module.
Handles initialization of the Gemini LLM model.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from config import (
    MODEL_NAME,
    MODEL_TEMPERATURE,
    MODEL_MAX_TOKENS,
    MODEL_TIMEOUT,
    MODEL_MAX_RETRIES,
)


def initialize_model(api_key: str) -> ChatGoogleGenerativeAI:
    """
    Initialize the Gemini model with specified configuration.

    Args:
        api_key (str): The Gemini API key

    Returns:
        ChatGoogleGenerativeAI: Initialized model instance
    """
    model = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=MODEL_TEMPERATURE,
        max_tokens=MODEL_MAX_TOKENS,
        timeout=MODEL_TIMEOUT,
        max_retries=MODEL_MAX_RETRIES,
        api_key=api_key,
    )
    return model
