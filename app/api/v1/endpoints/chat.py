from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.ai.chatbot import generate_chat_response


router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None


@router.post("/chat")
async def chat_endpoint(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await generate_chat_response(
        query=payload.query,
        db=db,
        session_id=payload.session_id
    )

    return result