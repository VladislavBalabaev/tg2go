from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Integer, Numeric, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.order_item import OrderItem


class Good(Base):
    __tablename__ = "goods"

    # --- primary key ---
    good_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    # --- description ---
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    short_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    price_rub: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    subcategory: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    image_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )  # TODO: more about it
    weight_grams: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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
    order_items: Mapped[list[OrderItem]] = relationship(back_populates="good")
