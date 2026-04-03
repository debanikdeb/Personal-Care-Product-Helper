from app.core.config import settings
import os


os.environ["langchain_endpoint"] = settings.LANGCHAIN_ENDPOINT
os.environ["langchain_api_key"] = settings.LANGCHAIN_API_KEY
os.environ["langchain_project"] = settings.LANGCHAIN_PROJECT
os.environ["langchain_tracing_v2"] = settings.LANGCHAIN_TRACING_V2
