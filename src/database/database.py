from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from src.config import config
from src.database.models import Base

async_engine = create_async_engine(
    config.ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

sync_engine = create_engine(
    config.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def init_db_sync():
    Base.metadata.create_all(sync_engine)