from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tg2go.db.base import Base
from tg2go.db.models.common.time import TimestampMixin
from tg2go.db.models.common.types import CategoryId

if TYPE_CHECKING:
    from tg2go.db.models.good import Good


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    # --- primary key ---
    category_id: Mapped[CategoryId] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    # --- description ---
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # --- relationship ---
    goods: Mapped[list[Good]] = relationship(
        "Good",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def GetStaffInfo(self) -> str:
        return f"- Название: {self.name}\n- Индекс: {self.index}\n- Содержит позиций: {len(self.goods)}\n\nЧем больше индекс, тем дальше категория в списке категорий."
