from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
import os
import constants
from app.api.v1.router import api_router



app = FastAPI(
    title="Personal Care Product Chatbot Backend",
    description="AI-powered personal care product Recommendation and Product Scraper",
    version=constants.API_VERSION,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


os.makedirs(settings.TEMP_PATH, exist_ok=True)

app.include_router(api_router, prefix=constants.API_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "Personal Care Chatbot app is running",
        "version": constants.API_VERSION,
    }



