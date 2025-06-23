from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import (
    StaffAction,
    StaffPosition,
    TextMenu,
)
from tg2go.db.models.common.types import CategoryId
from tg2go.services.staff.category import StaffCategoryService


class CategoryChangeAction(StaffAction):
    Name = "✏️ Изменить название"
    Index = "✏️ Изменить индекс"
    Back = "⬅️ Назад"


class CategoryChangeCallbackData(CallbackData, prefix="staff.cat.change"):
    action: CategoryChangeAction
    category_id: CategoryId


def CreateButton(action: StaffAction, category_id: CategoryId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=CategoryChangeCallbackData(
            action=action, category_id=category_id
        ).pack(),
    )


async def CategoryChangeMenu(category_id: CategoryId) -> TextMenu:
    cat_srv = StaffCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    text = f"🔴 Бот не работает\n\nО категории:\n{category.GetInfoForStaff()}{StaffPosition.Category(category)}"
    buttons = [
        [CreateButton(action=CategoryChangeAction.Name, category_id=category_id)],
        [CreateButton(action=CategoryChangeAction.Index, category_id=category_id)],
        [CreateButton(action=CategoryChangeAction.Back, category_id=category_id)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return TextMenu(
        text=text,
        reply_markup=markup,
    )
