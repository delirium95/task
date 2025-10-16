from sqlalchemy import select
from typing import Generic, TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model


    async def add_all(self, objects: list[T]):
        self.session.add_all(objects)
        await self.session.flush()

    async def add(self, object: T):
        self.session.add(object)
        await self.session.flush()

    async def get_all(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()