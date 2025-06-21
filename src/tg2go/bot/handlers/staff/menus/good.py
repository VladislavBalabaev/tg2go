from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import Menu, StaffAction
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.services.staff.category import StaffCategoryService
from tg2go.services.staff.good import StaffGoodService


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
    cat_srv = StaffCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    good_srv = StaffGoodService.Create()
    good = await good_srv.GetGood(good_id)

    text = f"🔴 Бот не работает\n\nВы находитесь в настройках продукта '{good.name}' категории '{category.name}'.\n\nО продукте:\n\n{good.GetStaffInfo()}"
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
