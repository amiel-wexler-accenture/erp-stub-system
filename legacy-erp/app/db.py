import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import Optional

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/legacy",
)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Active profile state (module-level, mutated on profile switch)
active_profile_id: str = "sap_ecc"
current_profile = None  # Will hold the active BaseProfile instance


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
