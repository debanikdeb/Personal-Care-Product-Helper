from sqlalchemy import Column, Integer, String
from .base import Base  # reuse same Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    benefits = Column(String, nullable=False)
    category = Column(String, nullable=False)  # skin/eye/lips/nails/face/hair