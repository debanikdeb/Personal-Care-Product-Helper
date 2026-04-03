import uuid
from langchain_groq import ChatGroq
from app.core.config import settings
from .prompts.helper import load_system_prompt, format_content_prompt
from app.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from constants import SUPPORT_CONTACT, SYSTEM_PROMPT_FILE_PATH, CHAT_MODEL
from langchain_core.messages import HumanMessage, AIMessage


chat_memory = {}


llm = ChatGroq(
    model=CHAT_MODEL,
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0.7,

)


async def fetch_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    context = "\n".join([
        f"{p.name} ({p.brand}) - ₹{p.price} | {p.category} | {p.benefits}"
        for p in products
    ])

    return context


async def generate_chat_response(query: str, db: AsyncSession, session_id: str = None):

    if not session_id:
        session_id = str(uuid.uuid4())

    # Get memory (last 5)
    history = chat_memory.get(session_id, [])[-5:]

    prompt_template = await load_system_prompt(
        "System Prompt",
        SYSTEM_PROMPT_FILE_PATH
    )

    context = await fetch_products(db)

    tool = "Database lookup for personal care products"

    final_prompt = format_content_prompt(
        prompt_template=prompt_template,
        context=context,
        query=query,
        tool=tool,
        contact_info=SUPPORT_CONTACT
    )

    messages = []

    # Convert history
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # Add current query
    messages.append(HumanMessage(content=final_prompt))

    llm_result = await llm.agenerate([messages])
    response = llm_result.generations[0][0].message.content

    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response})

    chat_memory[session_id] = history[-5:]

    return {
        "session_id": session_id,
        "response": response
    }