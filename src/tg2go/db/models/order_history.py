from __future__ import annotations

import logging
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    Text,
    event,
    insert,
)
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base

if TYPE_CHECKING:
    from tg2go.db.models.order import Order, OrderId, OrderStatus


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
    order: Mapped[Order] = relationship(back_populates="history")


@event.listens_for(Order, "after_insert", propagate=True)
def _SaveToOrderHistoryOnInsert(
    mapper: Any,
    connection: Connection,
    target: Order,
) -> None:
    stmt = insert(OrderHistory).values(
        order_id=target.order_id,
        chat_id=target.chat_id,
        status=target.status,
        total_price_rub=target.total_price_rub,
        internal_comment=target.internal_comment,
        client_comment=target.client_comment,
        updated_at=target.created_at,
    )
    connection.execute(stmt)

    logging.info(
        f"OrderItem(order_id={target.order_id}, updated_at={target.created_at}) is inserted upon order insertion."
    )


@event.listens_for(Order, "after_update", propagate=True)
def _SaveToOrderHistoryOnUpdate(
    mapper: Any,
    connection: Connection,
    target: Order,
) -> None:
    stmt = insert(OrderHistory).values(
        order_id=target.order_id,
        chat_id=target.chat_id,
        status=target.status,
        total_price_rub=target.total_price_rub,
        internal_comment=target.internal_comment,
        client_comment=target.client_comment,
        updated_at=target.updated_at,
    )

    connection.execute(stmt)

    logging.info(
        f"OrderItem(order_id={target.order_id}, updated_at={target.created_at}) is updated upon order update."
    )
