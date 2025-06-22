from dataclasses import dataclass
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


class ClientPosition:
    start = "\n\n🔹"

    class Label(str, Enum):
        Menu = "Меню"
        Cart = "Корзина"

    @classmethod
    def Path(cls, *args: str) -> str:
        parts = [f"[{i}]" for i in args]

        return cls.start + " > ".join(parts)

    @classmethod
    def Hub(cls) -> str:
        return cls.Path(cls.Label.Menu.value)

    @classmethod
    def Category(cls, category: Category) -> str:
        return cls.Path(cls.Label.Menu.value, category.name)

    @classmethod
    def Good(cls, good: Good) -> str:
        return cls.Path(cls.Label.Menu.value, good.category.name, good.name)

    @classmethod
    def Item(cls, item: OrderItem) -> str:
        return cls.Path(cls.Label.Menu.value, item.good.category.name, item.good.name)

    @classmethod
    def Cart(cls) -> str:
        return cls.Path(cls.Label.Cart.value)


@dataclass
class Menu:
    text: str
    reply_markup: InlineKeyboardMarkup | None
