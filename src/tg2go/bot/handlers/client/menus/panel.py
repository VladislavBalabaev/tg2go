from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import ClientAction, CreateButton, Menu


class PanelAction(ClientAction):
    Menu = "🍽️ Меню"
    Address = "📍 Местоположение"
    About = "🧭 О нас"
    AboutService = "🏢 О сервисе"
    Back = "⬅️ Назад"


class PanelCallbackData(CallbackData, prefix="client.panel"):
    action: PanelAction


def PanelMenu() -> Menu:
    # TODO
    text = "..."
    buttons = [
        [CreateButton(cb=PanelCallbackData, action=PanelAction.Menu)],
        [CreateButton(cb=PanelCallbackData, action=PanelAction.Address)],
        [CreateButton(cb=PanelCallbackData, action=PanelAction.About)],
        [CreateButton(cb=PanelCallbackData, action=PanelAction.AboutService)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )


def BackToPanelReplyMarkup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[CreateButton(cb=PanelCallbackData, action=PanelAction.Back)]]
    )
