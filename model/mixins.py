import uuid

from sqlalchemy import DateTime, func, UUID
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class TimestampMixin:
    @declared_attr
    def created_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, default=func.now(), onupdate=func.now())


class IdMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
