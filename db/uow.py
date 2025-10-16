import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import app_settings
from db.ContactRepository import ContactRepository

engine = create_async_engine(app_settings.db.db_url)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class UnitOfWork():
    async def __aenter__(self):
        self.session = AsyncSessionLocal()
        self.contacts = ContactRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
            logging.error(f"Error: {exc_val}, {exc_type}, {exc_tb}")
        else:
            await self.session.commit()
        await self.session.aclose()
