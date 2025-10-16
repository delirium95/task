import pytest
from sqlalchemy import text

from tests.test_uow import TestUnitOfWork


@pytest.mark.asyncio
async def test_async_session_connection():
    async with TestUnitOfWork() as uow:
        result = await uow.session.execute(text("SELECT 1"))
        scalar_result = result.scalar()
        assert scalar_result == 1, f"Expected 1, got {scalar_result}"
