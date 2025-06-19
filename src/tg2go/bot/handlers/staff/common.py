from dataclasses import dataclass
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class StaffAction(str, Enum):
    Cancel = "Оставить как есть"

    Activate = "Включить"
    Deactivate = "Выключить"
    Settings = "Настройки"

    Categories = "Категории"
    Goods = "Продукты"

    AddCategory = "Добавить"
    RemoveCategory = "Удалить"
    RenameCategory = "Переименовать"

    AddGood = "Добавить"
    # RemoveGood = "Удалить"
    # ChangeGood = "Изменить"


class StaffCallbackData(CallbackData, prefix="blocking"):
    action: StaffAction
    chat_id: int


def StaffKeyboard(actions: list[StaffAction], chat_id: int) -> InlineKeyboardMarkup:
    def Button(action: StaffAction) -> InlineKeyboardButton:
        nonlocal chat_id

        return InlineKeyboardButton(
            text=action.value,
            callback_data=StaffCallbackData(action=action, chat_id=chat_id).pack(),
        )

    buttons: list[InlineKeyboardButton] = [Button(a) for a in actions]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


class StaffHeaderText(str, Enum):
    Active = "🟢 Бот работает\n\nЧтобы поменять настройки бота, выключите его"
    Inactive = "🔴 Бот не работает"
    Category = ""


@dataclass
class StaffMenu:
    text: StaffHeaderText
    reply_markup: InlineKeyboardMarkup | None
