from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.db.populate_products import populate_products
from constants import PRODUCT_JSON_PATH


router = APIRouter()


@router.post("/populate-products")
async def populate_products_api(db: AsyncSession = Depends(get_db)):
    return await populate_products(
        db,
        PRODUCT_JSON_PATH
    )