from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base

if TYPE_CHECKING:
    from tg2go.db.models.order_history import OrderHistory
    from tg2go.db.models.order_item import OrderItem


# TODO: add more order statuses
class OrderStatus(str, Enum):
    created = "created"
    pending = "pending"
    paid = "paid"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    # --- primary key ---
    order_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    # --- secondary key ---
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("users.chat_id"),
        index=True,
    )

    # --- description ---
    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus),
        default=OrderStatus.created,
        nullable=False,
    )
    total_price_rub: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.0"),
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False,
    )

    # --- relationship ---
    order_items: Mapped[list[OrderItem]] = relationship(back_populates="order")
    history: Mapped[list[OrderHistory]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderHistory.changed_at",
    )


def CreateOrder(chat_id: int) -> Order:
    return Order(chat_id=chat_id)
