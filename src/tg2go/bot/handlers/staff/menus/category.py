from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.menu import Menu
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.db.models.good import Good
from tg2go.services.staff.good import StaffGoodService


class CategoryAction(str, Enum):
    AddGood = "Добавить продукт"
    ChangeCategory = "Изменить категорию"
    RemoveCategory = "Удалить категорию"
    Back = "Вернуться обратно"


class CategoryCallbackData(CallbackData, prefix="s.cat"):
    action: CategoryAction
    category_id: CategoryId
    chat_id: int


class CategoryGoodCallbackData(CallbackData, prefix="s.cat.good"):
    category_id: CategoryId
    good_id: GoodId
    chat_id: int


async def CategoryMenu(chat_id: int, category_id: CategoryId) -> Menu:
    srv = StaffGoodService.Create()
    goods: list[Good] = await srv.GetAvailableGoods(category_id)

    # TODO: add text
    text = "..."
    buttons = [
        [
            InlineKeyboardButton(
                text=CategoryAction.ChangeCategory.value,
                callback_data=CategoryCallbackData(
                    action=CategoryAction.ChangeCategory,
                    category_id=category_id,
                    chat_id=chat_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=CategoryAction.RemoveCategory.value,
                callback_data=CategoryCallbackData(
                    action=CategoryAction.RemoveCategory,
                    category_id=category_id,
                    chat_id=chat_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=CategoryAction.AddGood.value,
                callback_data=CategoryCallbackData(
                    action=CategoryAction.AddGood,
                    category_id=category_id,
                    chat_id=chat_id,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=good.name,
                callback_data=CategoryGoodCallbackData(
                    category_id=category_id,
                    good_id=good.good_id,
                    chat_id=chat_id,
                ).pack(),
            )
            for good in goods
        ],
        [
            InlineKeyboardButton(
                text=CategoryAction.Back.value,
                callback_data=CategoryCallbackData(
                    action=CategoryAction.Back,
                    category_id=category_id,
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

