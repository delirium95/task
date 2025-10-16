from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.ContactRepository import ContactRepository

TEST_DATABASE_URL = "sqlite+aiosqlite:///file::memory:?cache=shared"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

TestingSessionLocal = sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


class TestUnitOfWork:
    async def __aenter__(self):
        self.session = TestingSessionLocal()
        self.contacts = ContactRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.aclose()
