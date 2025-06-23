from dataclasses import dataclass
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from tg2go.db.models.category import Category
from tg2go.db.models.good import Good
from tg2go.db.models.order_item import OrderItem


class ClientAction(str, Enum):
    pass


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


@dataclass
class Menu:
    text: str
    reply_markup: InlineKeyboardMarkup | None


@dataclass
class MediaMenu:
    media: InputMediaPhoto
    reply_markup: InlineKeyboardMarkup | None


class ClientPosition:
    start = "\n\n\n🔹"

    class Label(str, Enum):
        Menu = "Меню"
        Cart = "Корзина"

    @classmethod
    def _Path(cls, *args: str) -> str:
        parts = [f"[{i}]" for i in args]

        return cls.start + " > ".join(parts)

    @classmethod
    def Hub(cls) -> str:
        return cls._Path(cls.Label.Menu.value)

    @classmethod
    def Category(cls, category: Category) -> str:
        return cls._Path(cls.Label.Menu.value, category.name)

    @classmethod
    def Good(cls, good: Good) -> str:
        return cls._Path(cls.Label.Menu.value, good.category.name, good.name)

    @classmethod
    def Item(cls, item: OrderItem) -> str:
        return cls._Path(cls.Label.Menu.value, item.good.category.name, item.good.name)

    @classmethod
    def Cart(cls) -> str:
        return cls._Path(cls.Label.Cart.value)


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
