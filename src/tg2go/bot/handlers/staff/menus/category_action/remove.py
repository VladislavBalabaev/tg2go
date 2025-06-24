from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import (
    Menu,
    StaffAction,
    StaffPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
from tg2go.db.models.common.types import CategoryId
from tg2go.services.staff.category import StaffCategoryService


class CategoryRemoveAction(StaffAction):
    Delete = "🗑️ Точно удалить"
    Back = "⬅️ Назад"


class CategoryRemoveCallbackData(CallbackData, prefix="staff.cat.remove"):
    action: CategoryRemoveAction
    category_id: CategoryId


def CreateButton(action: StaffAction, category_id: CategoryId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=CategoryRemoveCallbackData(
            action=action, category_id=category_id
        ).pack(),
    )


async def CategoryRemoveMenu(category_id: CategoryId) -> Menu:
    cat_srv = StaffCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    text = f"🔴 Бот не работает\n\nО категории:\n{category.GetInfoForStaff()}{StaffPosition.Category(category)}"
    buttons = [
        [CreateButton(action=CategoryRemoveAction.Delete, category_id=category_id)],
        [CreateButton(action=CategoryRemoveAction.Back, category_id=category_id)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
