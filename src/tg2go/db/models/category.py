from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin
from tg2go.db.models.common.types import CategoryId

if TYPE_CHECKING:
    from tg2go.db.models.good import Good


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
        "Good",
        back_populates="category",
        cascade="all, delete-orphan",
    )
