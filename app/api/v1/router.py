from fastapi import APIRouter
from app.api.v1.endpoints import product_ops
from app.api.v1.endpoints import chat
from app.api.v1.endpoints import extractor

api_router = APIRouter()


api_router.include_router(
    product_ops.router,
    prefix="/products",
    tags=["Products"]
)


api_router.include_router(
    chat.router,
    prefix="/chatbot",
    tags=["Chatbot"]
)



api_router.include_router(
    extractor.router,
    prefix="/extractor",
    tags=["Extractor"]
)
