from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import CreateButton, Menu, StaffAction
from tg2go.bot.lifecycle.active import bot_state


class PanelAction(StaffAction):
    Activate = "Включить"
    Deactivate = "Выключить"
    Settings = "Настройки"
    Cancel = "Оставить как есть"


class PanelCallbackData(CallbackData, prefix="staff.panel"):
    action: PanelAction


def PanelMenu() -> Menu:
    if bot_state.active:
        text = "🟢 Бот работает\n\nЧтобы поменять настройки бота, сперва выключите его"
        buttons = [
            [
                CreateButton(cb=PanelCallbackData, action=PanelAction.Deactivate),
            ],
            [
                CreateButton(cb=PanelCallbackData, action=PanelAction.Cancel),
            ],
        ]
    else:
        text = "🔴 Бот не работает"
        buttons = [
            [
                CreateButton(cb=PanelCallbackData, action=PanelAction.Activate),
            ],
            [
                CreateButton(cb=PanelCallbackData, action=PanelAction.Settings),
            ],
            [
                CreateButton(cb=PanelCallbackData, action=PanelAction.Cancel),
            ],
        ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
