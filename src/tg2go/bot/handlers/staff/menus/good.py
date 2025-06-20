from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import Menu, StaffAction
from tg2go.db.models.common.types import CategoryId, GoodId


class GoodAction(StaffAction):
    ChangeGood = "Изменить продукт"
    RemoveGood = "Удалить продукт"
    Back = "Вернуться обратно"


class GoodCallbackData(CallbackData, prefix="s.good"):
    action: GoodAction
    category_id: CategoryId
    good_id: GoodId


def CreateButton(
    action: StaffAction, category_id: CategoryId, good_id: GoodId
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=GoodCallbackData(
            action=action,
            category_id=category_id,
            good_id=good_id,
        ).pack(),
    )


async def GoodMenu(category_id: CategoryId, good_id: GoodId) -> Menu:
    # TODO: add text
    text = "..."
    buttons = [
        [
            CreateButton(
                action=GoodAction.ChangeGood,
                category_id=category_id,
                good_id=good_id,
            ),
            CreateButton(
                action=GoodAction.RemoveGood,
                category_id=category_id,
                good_id=good_id,
            ),
        ],
        [
            CreateButton(
                action=GoodAction.Back,
                category_id=category_id,
                good_id=good_id,
            ),
        ],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
