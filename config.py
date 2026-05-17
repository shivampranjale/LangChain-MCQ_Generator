"""
Configuration module for MCQ Generator.
Contains settings for API keys, model parameters, and file paths.
"""

from pathlib import Path
from getpass import getpass


# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# File paths
DEFAULT_PDF_PATH = None  # Will be set at runtime

# Model configuration
MODEL_NAME = "gemini-3.1-flash-lite"
MODEL_TEMPERATURE = 0
MODEL_MAX_TOKENS = None
MODEL_TIMEOUT = None
MODEL_MAX_RETRIES = 2

# Default topic domain
DEFAULT_TOPIC_DOMAIN = "Prompt Engineering Domain"


def get_api_key():
    """Get Gemini API key from user input."""
    return getpass('Enter Gemini API Key: ')


def get_pdf_path():
    """Get PDF file path from user input."""
    return input("Enter the path to the PDF file: ")
