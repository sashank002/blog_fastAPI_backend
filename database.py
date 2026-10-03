from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os

BASE_DIR = Path(__file__).resolve().parent

SQLALCHEMY_DATABASE_URI = os.getenv(
         "DATABASE_URL",
    f"sqlite+aiosqlite:///{BASE_DIR / 'blog.db'}" 
     )

# Hosts like Railway/Render give a plain "postgresql://" (or legacy "postgres://")
# URL, which SQLAlchemy maps to the sync psycopg2 driver. We need the async driver.
for prefix in ("postgres://", "postgresql://"):
    if SQLALCHEMY_DATABASE_URI.startswith(prefix):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(prefix, "postgresql+asyncpg://", 1)
        break


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