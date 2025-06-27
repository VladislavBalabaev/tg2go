from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Enum as SqlEnum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin
from tg2go.db.models.common.types import OrderId, OrderStatus

if TYPE_CHECKING:
    from tg2go.db.models.order_history import OrderHistory
    from tg2go.db.models.order_item import OrderItem


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    # --- primary key ---
    order_id: Mapped[OrderId] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    # --- secondary key ---
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("users.chat_id"),
        index=True,
        nullable=False,
    )

    # --- messages ---
    order_message_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
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
    internal_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    client_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # --- relationship ---
    order_items: Mapped[list[OrderItem]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    history: Mapped[list[OrderHistory]] = relationship(
        "OrderHistory",
        back_populates="order",
    )

    def GetClientInfo(self) -> str:
        info = "Шаурма / Сетунь\n📍Москва, ул. Толбухина, 13А, корп. 3\n\n"

        if not self.order_items:
            info += "Ваш заказ пока что пуст."
            return info

        info += "Заказ:\n"

        for i, item in enumerate(self.order_items, 1):
            name: str = item.good.name
            qty: int = item.quantity
            price: Decimal = item.unit_price_rub

            info += f"{i}. {name}, {qty} шт. × {price}₽ = {price * qty}₽\n"

        info += f"\nИтого: {self.total_price_rub}₽"

        return info
