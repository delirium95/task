import pytest
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from services.import_service import ImportService
from tests.test_uow import TestUnitOfWork
from config.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///file::memory:?cache=shared"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_import_data(tmp_path):
    # створюємо тимчасовий Excel-файл
    df = pd.DataFrame([
        {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "description": "CEO"},
        {"first_name": "Bob", "last_name": "Brown", "email": "bob@example.com", "description": "CTO"},
    ])
    file_path = tmp_path / "contacts.xlsx"
    df.to_excel(file_path, index=False)

    uow = TestUnitOfWork()
    service = ImportService(uow=uow)
    await service.import_data(file_path)
    async with uow as u:
        contacts = await u.contacts.get_all()
        assert len(contacts) == 2
        assert contacts[0].first_name == "Alice"
