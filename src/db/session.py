from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

# Convert PostgreSQL URL to async format
async_database_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

async_engine = create_async_engine(
    async_database_url,
    pool_pre_ping=True,
    # Connection pool configuration for high concurrency
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
