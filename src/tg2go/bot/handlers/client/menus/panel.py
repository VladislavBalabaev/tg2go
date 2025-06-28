from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import ClientAction, ClientMenu
from tg2go.bot.lib.message.image import GetHeaderDir


class PanelAction(ClientAction):
    Menu = "🍽️ Меню"
    Address = "📍 Местоположение"
    About = "🧭 О нас"
    AboutService = "🏢 О сервисе"
    Back = "⬅️ Назад"


class PanelCallbackData(CallbackData, prefix="client.panel"):
    action: PanelAction


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


def PanelMenu() -> ClientMenu:
    address_url = (
        "https://yandex.ru/maps/org/shaurma/240778331973/?ll=37.396586%2C55.722892&z=17"
    )

    text = ""
    buttons = [
        [CreateButton(cb=PanelCallbackData, action=PanelAction.Menu)],
        [
            InlineKeyboardButton(
                text=PanelAction.Address.value,
                url=address_url,
            )
        ],
        [CreateButton(cb=PanelCallbackData, action=PanelAction.About)],
        [CreateButton(cb=PanelCallbackData, action=PanelAction.AboutService)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )


def PanelMenuExplain(text: str) -> ClientMenu:
    buttons = [[CreateButton(cb=PanelCallbackData, action=PanelAction.Back)]]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
