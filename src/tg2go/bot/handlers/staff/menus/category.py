from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import Menu, StaffAction
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.db.models.good import Good
from tg2go.services.staff.good import StaffGoodService


class CategoryAction(StaffAction):
    AddGood = "Добавить продукт"
    ChangeCategory = "Изменить категорию"
    RemoveCategory = "Удалить категорию"
    Back = "Вернуться обратно"


class CategoryCallbackData(CallbackData, prefix="staff.cat"):
    action: CategoryAction
    category_id: CategoryId


class CategoryGoodCallbackData(CallbackData, prefix="staff.cat.good"):
    category_id: CategoryId
    good_id: GoodId


def CreateButton(action: StaffAction, category_id: CategoryId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=CategoryCallbackData(
            action=action, category_id=category_id
        ).pack(),
    )


async def CategoryMenu(category_id: CategoryId) -> Menu:
    srv = StaffGoodService.Create()
    goods: list[Good] = await srv.GetAvailableGoods(category_id)

    # TODO: add text
    text = "..."
    buttons = [
        [
            CreateButton(action=CategoryAction.ChangeCategory, category_id=category_id),
            CreateButton(action=CategoryAction.RemoveCategory, category_id=category_id),
        ],
        [
            CreateButton(action=CategoryAction.AddGood, category_id=category_id),
        ],
        [
            InlineKeyboardButton(
                text=good.name,
                callback_data=CategoryGoodCallbackData(
                    category_id=category_id,
                    good_id=good.good_id,
                ).pack(),
            )
            for good in goods
        ],
        [
            CreateButton(action=CategoryAction.Back, category_id=category_id),
        ],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
