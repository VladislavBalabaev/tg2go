from __future__ import annotations

from typing import TYPE_CHECKING, NewType
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin

if TYPE_CHECKING:
    from tg2go.db.models.good import Good


CategoryId = NewType("CategoryId", UUID)
GoodId = NewType("GoodId", UUID)


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    # --- primary key ---
    category_id: Mapped[CategoryId] = mapped_column(
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    # --- description ---
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # --- relationship ---
    goods: Mapped[list[Good]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )
