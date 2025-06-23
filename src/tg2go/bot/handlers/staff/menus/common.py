from dataclasses import dataclass
from enum import Enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from tg2go.db.models.category import Category
from tg2go.db.models.good import Good


class StaffAction(str, Enum):
    pass


@dataclass
class TextMenu:
    text: str
    reply_markup: InlineKeyboardMarkup | None


@dataclass
class MediaMenu:
    media: InputMediaPhoto
    reply_markup: InlineKeyboardMarkup | None


class StaffPosition:
    start = "\n\n\n🔹"

    class Label(str, Enum):
        Settings = "Настройки"

    @classmethod
    def _Path(cls, *args: str) -> str:
        parts = [f"[{i}]" for i in args]

        return cls.start + " > ".join(parts)

    @classmethod
    def Settings(cls) -> str:
        return cls._Path(cls.Label.Settings.value)

    @classmethod
    def Category(cls, category: Category) -> str:
        return cls._Path(cls.Label.Settings.value, category.name)

    @classmethod
    def Good(cls, good: Good) -> str:
        return cls._Path(cls.Label.Settings.value, good.category.name, good.name)


def SplitButtonsInTwoColumns(
    plain_buttons: list[InlineKeyboardButton],
) -> list[list[InlineKeyboardButton]]:
    new_buttons = []

    group = []
    for i, button in enumerate(plain_buttons):
        group.append(button)

        if i % 2 == 1:
            new_buttons.append(group)
            group = []

    if group:
        new_buttons.append(group)

    return new_buttons
