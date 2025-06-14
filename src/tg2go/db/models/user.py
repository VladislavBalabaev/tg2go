from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from tg2go.db.base import Base


class User(Base):
    __tablename__ = "users"

    # --- primary key ---
    chat_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    # --- secondary keys ---
    username: Mapped[str] = mapped_column(
        Text,
        index=True,
        nullable=True,
    )
    phone_number: Mapped[str] = mapped_column(
        Text,
        index=True,
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
