import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product


async def populate_products(db: AsyncSession, file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)

    products = [
        Product(
            name=item["name"],
            brand=item["brand"],
            price=item["price"],
            benefits=item["benefits"],
            category=item["category"]
        )
        for item in data
    ]

    db.add_all(products)
    await db.commit()

    return {"message": f"{len(products)} products inserted"}