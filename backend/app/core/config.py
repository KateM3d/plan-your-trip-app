import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Plan Your Trip"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()
