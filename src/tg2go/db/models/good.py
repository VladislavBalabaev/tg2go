from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, NewType
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin

if TYPE_CHECKING:
    from tg2go.db.models.category import Category
    from tg2go.db.models.order_item import OrderItem


GoodId = NewType("GoodId", UUID)


class Good(Base, TimestampMixin):
    __tablename__ = "goods"

    # --- primary key ---
    good_id: Mapped[GoodId] = mapped_column(
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    # --- description ---
    price_rub: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    short_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    image_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )  # TODO: more about it
    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # --- relationship ---
    category: Mapped[Category] = relationship(back_populates="goods")

    order_items: Mapped[list[OrderItem]] = relationship(
        back_populates="good",
        cascade="all, delete-orphan",
    )
