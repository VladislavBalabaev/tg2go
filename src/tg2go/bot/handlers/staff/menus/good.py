from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.menu import Menu
from tg2go.db.models.common.types import CategoryId, GoodId


class GoodAction(str, Enum):
    ChangeGood = "Изменить продукт"
    RemoveGood = "Удалить продукт"
    Back = "Вернуться обратно"


class GoodCallbackData(CallbackData, prefix="s.good"):
    action: GoodAction
    category_id: CategoryId
    good_id: GoodId
    chat_id: int


async def GoodMenu(chat_id: int, category_id: CategoryId, good_id: GoodId) -> Menu:
    # TODO: add text
    text = "..."
    buttons = [
        [
            InlineKeyboardButton(
                text=GoodAction.ChangeGood.value,
                callback_data=GoodCallbackData(
                    action=GoodAction.ChangeGood,
                    category_id=category_id,
                    good_id=good_id,
                    chat_id=chat_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=GoodAction.RemoveGood.value,
                callback_data=GoodCallbackData(
                    action=GoodAction.RemoveGood,
                    category_id=category_id,
                    good_id=good_id,
                    chat_id=chat_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=GoodAction.Back.value,
                callback_data=GoodCallbackData(
                    action=GoodAction.Back,
                    category_id=category_id,
                    good_id=good_id,
                    chat_id=chat_id,
                ).pack(),
            )
        ],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )