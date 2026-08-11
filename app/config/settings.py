import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Application Name
    APP_NAME: str = os.getenv("APP_NAME")

    # MODEL INITIALIZATION
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")

    # INITIALIZING GEMIN API KEY
    GEMINII_API_KEY: str = os.getenv("GEMINI_API_KEY")

    # Tokenization
    TOKENIZER_MODEL: str = os.getenv("TOKENIZER_MODEL")

    # Max Content Token
    MAX_CONTEXT_TOKENS: int = int(os.getenv("MAX_CONTEXT_TOKENS"))


# Creating an instance of Settings
settings = Settings()
