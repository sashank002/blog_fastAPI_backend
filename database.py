from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os

BASE_DIR = Path(__file__).resolve().parent

SQLALCHEMY_DATABASE_URI = os.getenv(
         "DATABASE_URL",
    f"sqlite+aiosqlite:///{BASE_DIR / 'blog.db'}" 
     )


# check_same_thread is SQLite-only — PostgreSQL doesn't support it
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URI else {}

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
    )

AsyncSessionLocal = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session