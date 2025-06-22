from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientPosition,
    CreateButton,
    Menu,
)
from tg2go.services.client.order import ClientOrderService


class CardAction(ClientAction):
    Pay = "🧾 Оплатить"
    InHub = "🍽️ В меню"


class CardCallbackData(CallbackData, prefix="client.card"):
    action: CardAction


async def CardMenu(chat_id: int) -> Menu:
    order_srv = await ClientOrderService.Create(chat_id)

    text = await order_srv.GetOrderInfo() + ClientPosition.Cart()
    buttons = [
        [CreateButton(cb=CardCallbackData, action=CardAction.Pay)],
        [CreateButton(cb=CardCallbackData, action=CardAction.InHub)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
