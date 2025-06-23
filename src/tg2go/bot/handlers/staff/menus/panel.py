from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import StaffAction, TextMenu
from tg2go.bot.lifecycle.active import bot_state


class PanelAction(StaffAction):
    Activate = "🚀 Включить бота"
    Deactivate = "💤 Выключить бота"
    Settings = "🛠️ Настройки"
    Exit = "Выйти из меню"


class PanelCallbackData(CallbackData, prefix="staff.panel"):
    action: PanelAction


def CreateButton(cb: type[CallbackData], action: StaffAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


def PanelMenu() -> TextMenu:
    if bot_state.active:
        text = "🟢 Бот работает и принимает заказы\n\nЧтобы поменять настройки бота, сперва выключите его"
        buttons = [
            [CreateButton(cb=PanelCallbackData, action=PanelAction.Deactivate)],
            [CreateButton(cb=PanelCallbackData, action=PanelAction.Exit)],
        ]
    else:
        text = "🔴 Бот не работает\n\nПользователи не могут создать заказ"
        buttons = [
            [CreateButton(cb=PanelCallbackData, action=PanelAction.Activate)],
            [CreateButton(cb=PanelCallbackData, action=PanelAction.Settings)],
            [CreateButton(cb=PanelCallbackData, action=PanelAction.Exit)],
        ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return TextMenu(
        text=text,
        reply_markup=markup,
    )
