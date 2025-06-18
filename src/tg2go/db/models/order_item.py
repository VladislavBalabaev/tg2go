from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin

if TYPE_CHECKING:
    from tg2go.db.models.good import Good, GoodId
    from tg2go.db.models.order import Order, OrderId


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    # --- primary key ---
    order_item_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # --- dependency ---
    order_id: Mapped[OrderId] = mapped_column(
        ForeignKey("orders.order_id"),
    )
    good_id: Mapped[GoodId] = mapped_column(
        ForeignKey("goods.good_id"),
    )

    # --- description ---
    quantity: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )
    unit_price_rub: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # --- relationship ---
    order: Mapped[Order] = relationship(back_populates="order_items")
    good: Mapped[Good] = relationship(back_populates="order_items")
