import os
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no ambiente")

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session