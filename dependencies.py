from contextlib import asynccontextmanager

from fastapi import Depends

from db.uow import AsyncSessionLocal, UnitOfWork
from services.import_service import ImportService


@asynccontextmanager
async def get_db_dependency():
    async with AsyncSessionLocal() as session:
        yield session


async def get_uow():
    async with UnitOfWork() as uow:
        yield uow


async def get_import_service(uow: UnitOfWork = Depends(get_uow)):
    yield ImportService(uow)
