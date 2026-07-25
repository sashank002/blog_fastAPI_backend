from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

BASE_DIR = Path(__file__).resolve().parent
SQLALCHEMY_DATABASE_URI = f"sqlite+aiosqlite:///{BASE_DIR / 'blog.db'}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    )

AsyncSessionLocal = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session