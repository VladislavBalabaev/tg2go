from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.good import Good
from tg2go.db.models.order import Order


class OrderItem(Base):
    __tablename__ = "order_items"

    # --- primary key ---
    item_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # --- dependency ---
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.order_id"),
    )
    good_id: Mapped[UUID] = mapped_column(
        ForeignKey("goods.good_id"),
    )

    # --- description ---
    quantity: Mapped[int] = mapped_column(
        default=1,
    )
    unit_price_rub: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # --- time ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    # --- relationship ---
    order: Mapped[Order] = relationship(back_populates="order_items")
    good: Mapped[Good] = relationship(back_populates="order_items")
