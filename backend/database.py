from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

# Check if DATABASE_URL is properly configured
if not DATABASE_URL or DATABASE_URL == "postgresql+asyncpg://user:password@host:port/database":
    # Use SQLite for testing when no real DATABASE_URL is provided
    DATABASE_URL = "sqlite+aiosqlite:///./test_database.db"
    print("⚠️ Using SQLite for testing - no valid PostgreSQL DATABASE_URL found")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=20 if DATABASE_URL.startswith("postgresql") else 5,
    max_overflow=0
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for all models
class Base(DeclarativeBase):
    pass

# Dependency to get database session
async def get_db_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()