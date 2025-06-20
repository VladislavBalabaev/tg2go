from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin
from tg2go.db.models.common.types import CategoryId, GoodId

if TYPE_CHECKING:
    from tg2go.db.models.category import Category
    from tg2go.db.models.order_item import OrderItem


class Good(Base, TimestampMixin):
    __tablename__ = "goods"

    # --- primary key ---
    good_id: Mapped[GoodId] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    # --- primary keys ---
    category_id: Mapped[CategoryId] = mapped_column(
        ForeignKey("categories.category_id"),
        index=True,
        nullable=False,
    )

    # --- description ---
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    price_rub: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
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
    category: Mapped[Category] = relationship(
        "Category",
        back_populates="goods",
    )

    order_items: Mapped[list[OrderItem]] = relationship(
        "OrderItem",
        back_populates="good",
        cascade="all, delete-orphan",
    )
