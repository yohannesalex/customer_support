# Import necessary components for asynchronous database interaction.
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from support_assistant_backend.core.config import settings

# Create an asynchronous database engine using the URL from settings.
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
# Configure an asynchronous sessionmaker to create database sessions.
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

# Define a dependency to yield an asynchronous database session, ensuring it's closed afterwards.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session