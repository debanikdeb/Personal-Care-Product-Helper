from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.utils.logger import logger
from sqlalchemy.exc import OperationalError, DBAPIError





engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=20,
    max_overflow=10,
    pool_timeout=60,
    pool_recycle=1800,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            logger.info("Database session created successfully.")
            yield session
    except (OperationalError, DBAPIError):
        async with AsyncSessionLocal() as session:
            logger.error("Database connection error. Retrying session creation.")
            yield session


