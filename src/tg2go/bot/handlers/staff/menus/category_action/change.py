from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import (
    StaffAction,
    StaffMenu,
    StaffPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
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


async def CategoryChangeMenu(category_id: CategoryId) -> StaffMenu:
    cat_srv = StaffCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    text = f"🔴 Бот не работает\n\nО категории:\n{category.GetStaffInfo()}{StaffPosition.Category(category)}"
    buttons = [
        [CreateButton(action=CategoryChangeAction.Name, category_id=category_id)],
        [CreateButton(action=CategoryChangeAction.Index, category_id=category_id)],
        [CreateButton(action=CategoryChangeAction.Back, category_id=category_id)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return StaffMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
