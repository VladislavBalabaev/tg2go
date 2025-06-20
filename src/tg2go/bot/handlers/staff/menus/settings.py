from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import CreateButton, Menu, StaffAction
from tg2go.db.models.common.types import CategoryId
from tg2go.services.staff.category import StaffCategoryService


class SettingsAction(StaffAction):
    AddCategory = "Добавить категорию"
    Back = "Вернуться обратно"


class SettingsCallbackData(CallbackData, prefix="staff.settings"):
    action: SettingsAction


class SettingsCategoryCallbackData(CallbackData, prefix="staff.settings.cat"):
    category_id: CategoryId


async def SettingsMenu() -> Menu:
    srv = StaffCategoryService.Create()
    categories = await srv.GetSortedCategories()

    # TODO: add text
    text = "🔴 Бот не работает\n\nВы находитесь в настройках бота.\n..."
    buttons = [
        [
            CreateButton(cb=SettingsCallbackData, action=SettingsAction.AddCategory),
        ],
        [
            InlineKeyboardButton(
                text=cat.name,
                callback_data=SettingsCategoryCallbackData(
                    category_id=cat.category_id
                ).pack(),
            )
            for cat in categories
        ],
        [
            CreateButton(cb=SettingsCallbackData, action=SettingsAction.Back),
        ],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
