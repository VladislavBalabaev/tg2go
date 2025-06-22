from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import CreateButton, Menu, StaffAction
from tg2go.db.models.common.types import CategoryId
from tg2go.services.staff.category import StaffCategoryService


class SettingsAction(StaffAction):
    AddCategory = "🍽️ Добавить категорию"
    Back = "⬅️ Назад"


class SettingsCallbackData(CallbackData, prefix="staff.settings"):
    action: SettingsAction


class SettingsCategoryCallbackData(CallbackData, prefix="staff.settings.cat"):
    category_id: CategoryId


async def SettingsMenu() -> Menu:
    srv = StaffCategoryService.Create()
    categories = await srv.GetSortedCategories()

    buttons = []

    group = []
    for i, cat in enumerate(categories):
        group.append(
            InlineKeyboardButton(
                text=cat.name,
                callback_data=SettingsCategoryCallbackData(
                    category_id=cat.category_id
                ).pack(),
            )
        )

        if i % 2 == 1:
            buttons.append(group)
            group = []

    if group:
        buttons.append(group)

    # TODO: add text
    text = "..."
    buttons = [
        [CreateButton(cb=SettingsCallbackData, action=SettingsAction.AddCategory)],
        *buttons,
        [CreateButton(cb=SettingsCallbackData, action=SettingsAction.Back)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
