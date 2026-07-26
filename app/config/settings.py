import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Application Name
    APP_NAME: str = os.getenv("APP_NAME")

    # MODEL INITIALIZATION
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER")
    MODEL_NAME: str = os.getenv("MODEL_NAME")

    # INITIALIZING GEMIN API KEY
    GEMINII_API_KEY: str = os.getenv("GEMINI_API_KEY")


# Creating an instance of Settings
settings = Settings()
