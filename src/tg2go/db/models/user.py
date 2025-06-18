from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin

if TYPE_CHECKING:
    from tg2go.db.models.order import OrderId


class User(Base, TimestampMixin):
    __tablename__ = "users"

    # --- primary key ---
    chat_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    # --- secondary keys ---
    username: Mapped[str | None] = mapped_column(
        Text,
        index=True,
        nullable=True,
    )
    phone_number: Mapped[str | None] = mapped_column(
        Text,
        index=True,
        nullable=True,
    )

    # --- order ---
    order_id: Mapped[OrderId | None] = mapped_column(
        nullable=True,
    )

    # --- state ---
    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
