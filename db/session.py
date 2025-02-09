from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'sqlite_aiosqlite:///./new_library.db'

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=engine, class_=AsyncSession
)


async def get_session():
    async with SessionLocal() as session:
        yield session
