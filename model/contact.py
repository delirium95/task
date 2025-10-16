from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config import Base
from model.mixins import IdMixin, TimestampMixin


class Contact(Base, IdMixin, TimestampMixin):
    __tablename__ = "contacts"

    first_name: Mapped[str] = mapped_column(String(1000))
    last_name: Mapped[str] = mapped_column(String(1000))
    email: Mapped[str] = mapped_column(String(1000))
    description: Mapped[str] = mapped_column(String(1000))
