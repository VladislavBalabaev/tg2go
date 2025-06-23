from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import (
    SplitButtonsInTwoColumns,
    StaffAction,
    StaffPosition,
    TextMenu,
)
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.services.staff.category import StaffCategoryService
from tg2go.services.staff.good import StaffGoodService


class CategoryAction(StaffAction):
    AddGood = "🥗 Добавить позицию"
    ChangeCategory = "✏️ Изменить категорию"
    RemoveCategory = "🗑️ Удалить категорию"
    Back = "⬅️ Назад"


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


async def CategoryMenu(category_id: CategoryId) -> TextMenu:
    cat_srv = StaffCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    good_srv = StaffGoodService.Create()
    goods = await good_srv.GetAvailableGoods(category_id)

    plain_buttons = [
        InlineKeyboardButton(
            text=good.name,
            callback_data=CategoryGoodCallbackData(
                category_id=category_id,
                good_id=good.good_id,
            ).pack(),
        )
        for good in goods
    ]

    text = f"🔴 Бот не работает\n\nО категории:\n{category.GetInfoForStaff()}{StaffPosition.Category(category)}"
    buttons = [
        [
            CreateButton(action=CategoryAction.ChangeCategory, category_id=category_id),
            CreateButton(action=CategoryAction.RemoveCategory, category_id=category_id),
        ],
        [CreateButton(action=CategoryAction.AddGood, category_id=category_id)],
        *SplitButtonsInTwoColumns(plain_buttons),
        [CreateButton(action=CategoryAction.Back, category_id=category_id)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return TextMenu(
        text=text,
        reply_markup=markup,
    )
