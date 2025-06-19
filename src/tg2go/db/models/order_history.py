from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.types import OrderId, OrderStatus

if TYPE_CHECKING:
    from tg2go.db.models.order import Order


class OrderHistory(Base):
    __tablename__ = "order_history"

    # --- primary key ---
    history_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # --- secondary key ---
    order_id: Mapped[OrderId] = mapped_column(
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("users.chat_id"),
        index=True,
        nullable=False,
    )

    # --- description ---
    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus),
        nullable=False,
    )
    total_price_rub: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    internal_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    client_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # --- time ---
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # --- relationship ---
    order: Mapped[Order] = relationship(
        "Order",
        back_populates="history",
    )
