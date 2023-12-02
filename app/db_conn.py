from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import POSTGRES_URI

DBBase = declarative_base()
metadata = DBBase.metadata
engine = create_async_engine(
    POSTGRES_URI,
    # echo=True,
    future=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False,
                                   autoflush=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
