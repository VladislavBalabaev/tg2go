from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
from tg2go.services.client.order import ClientOrderService


class CardAction(ClientAction):
    Pay = "🧾 Оплатить"
    InHub = "🍽️ В меню"


class CardCallbackData(CallbackData, prefix="client.card"):
    action: CardAction


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


async def CardMenu(chat_id: int) -> ClientMenu:
    order_srv = await ClientOrderService.Create(chat_id)
    order = await order_srv.GetOrder()

    text = order.GetClientInfo() + ClientPosition.Cart()
    buttons = [
        [CreateButton(cb=CardCallbackData, action=CardAction.Pay)],
        [CreateButton(cb=CardCallbackData, action=CardAction.InHub)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
