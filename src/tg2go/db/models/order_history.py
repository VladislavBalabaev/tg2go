from __future__ import annotations

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
    inspect,
)
from sqlalchemy.ext.asyncio import AsyncSession
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

    # --- description ---
    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus),
        nullable=False,
    )
    total_price_rub: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    internal_comment: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    client_comment: Mapped[str] = mapped_column(
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


@event.listens_for(AsyncSession, "before_flush")
def SaveToOrderHistory(
    session: AsyncSession,
    flush_context: Any,
    instances: Any,
) -> None:
    for obj in session.dirty:
        if not isinstance(obj, Order):
            continue
        order = obj

        state = inspect(order)
        if not state.attrs.updated_at.history.has_changes():
            continue

        now = datetime.now()  # noqa: DTZ005
        order.updated_at = now

        session.add(
            OrderHistory(
                status=order.status,
                total_price_rub=order.total_price_rub,
                internal_comment=order.internal_comment,
                client_comment=order.client_comment,
                updated_at=order.updated_at,
                order=order,
            )
        )
