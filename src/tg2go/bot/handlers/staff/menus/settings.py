from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import (
    SplitButtonsInTwoColumns,
    StaffAction,
    StaffMenu,
    StaffPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
from tg2go.db.models.common.types import CategoryId
from tg2go.services.staff.category import StaffCategoryService


class SettingsAction(StaffAction):
    AddCategory = "➕ Добавить категорию"
    Back = "⬅️ Назад"


class SettingsCallbackData(CallbackData, prefix="staff.settings"):
    action: SettingsAction


class SettingsCategoryCallbackData(CallbackData, prefix="staff.settings.cat"):
    category_id: CategoryId


def CreateButton(cb: type[CallbackData], action: StaffAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


async def SettingsMenu() -> StaffMenu:
    srv = StaffCategoryService.Create()
    categories = await srv.GetSortedCategories()

    plain_buttons = [
        InlineKeyboardButton(
            text=cat.name,
            callback_data=SettingsCategoryCallbackData(
                category_id=cat.category_id
            ).pack(),
        )
        for cat in categories
    ]

    text = "🔴 Бот не работает" + StaffPosition.Settings()
    buttons = [
        [CreateButton(cb=SettingsCallbackData, action=SettingsAction.AddCategory)],
        *SplitButtonsInTwoColumns(plain_buttons),
        [CreateButton(cb=SettingsCallbackData, action=SettingsAction.Back)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return StaffMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
