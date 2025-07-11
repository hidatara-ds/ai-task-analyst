import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    OPENAI_KEY: str = os.getenv("OPENAI_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    API_KEY: str = os.getenv("API_KEY", "")


settings = Settings()
