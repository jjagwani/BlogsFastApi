from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)