from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.menu import Menu
from tg2go.bot.lifecycle.active import bot_state


class StaffAction(str, Enum):
    Activate = "Включить"
    Deactivate = "Выключить"
    Settings = "Настройки"
    Cancel = "Оставить как есть"


class StaffCallbackData(CallbackData, prefix="s"):
    action: StaffAction
    chat_id: int


class StaffButtonFactory:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def Get(self, action: StaffAction) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=action.value,
            callback_data=StaffCallbackData(
                action=action,
                chat_id=self.chat_id,
            ).pack(),
        )


def StaffMenu(chat_id: int) -> Menu:
    factory = StaffButtonFactory(chat_id)

    if bot_state.active:
        text = "🟢 Бот работает\n\n"
        "Чтобы поменять настройки бота, сперва выключите его"
        buttons = [
            [factory.Get(StaffAction.Deactivate)],
            [factory.Get(StaffAction.Cancel)],
        ]
    else:
        text = "🔴 Бот не работает"
        buttons = [
            [factory.Get(StaffAction.Activate)],
            [factory.Get(StaffAction.Settings)],
            [factory.Get(StaffAction.Cancel)],
        ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )

