from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    ENV: str = config("ENV")
    FRONTEND_URL: str = config("FRONTEND_URL")
    BACKEND_URL: str = config("BACKEND_URL")
    DATABASE_URL: str = config("DATABASE_URL")
    GROQ_API_KEY: str = config("GROQ_API_KEY")
    LANGCHAIN_ENDPOINT: str = config("LANGCHAIN_ENDPOINT")
    LANGCHAIN_API_KEY: str = config("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: str = config("LANGCHAIN_PROJECT")
    LANGCHAIN_TRACING_V2: str = config("LANGCHAIN_TRACING_V2")
    TEMP_PATH: str = config("TEMP_PATH")

settings = Settings()