from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.menu import Menu
from tg2go.db.models.common.types import CategoryId
from tg2go.services.staff.category import StaffCategoryService


class SettingsAction(str, Enum):
    AddCategory = "Добавить категорию"
    Back = "Вернуться обратно"


class SettingsCallbackData(CallbackData, prefix="s.settings"):
    action: SettingsAction
    chat_id: int


class SettingsCategoryCallbackData(CallbackData, prefix="s.settings.cat"):
    category_id: CategoryId
    chat_id: int


async def SettingsMenu(chat_id: int) -> Menu:
    srv = StaffCategoryService.Create()
    categories = await srv.GetSortedCategories()

    # TODO: add text
    text = "🔴 Бот не работает\n\nВы находитесь в настройках бота.\n..."
    buttons = [
        [
            InlineKeyboardButton(
                text=SettingsAction.AddCategory.value,
                callback_data=SettingsCallbackData(
                    action=SettingsAction.AddCategory,
                    chat_id=chat_id,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=cat.name,
                callback_data=SettingsCategoryCallbackData(
                    category_id=cat.category_id,
                    chat_id=chat_id,
                ).pack(),
            )
            for cat in categories
        ],
        [
            InlineKeyboardButton(
                text=SettingsAction.Back.value,
                callback_data=SettingsCallbackData(
                    action=SettingsAction.Back,
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