from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
)
from tg2go.bot.lib.message.image import GetClientHeaderDir
from tg2go.services.client.order import ClientOrderService


class CartAction(ClientAction):
    Pay = "🧾 Оплатить"  # TODO: check wether chosen items are available now
    Change = "✏️ Редактировать"
    Clean = "♻️ Отчистить корзину"
    InHub = "🍽️ В меню"


class CartCallbackData(CallbackData, prefix="client.cart"):
    action: CartAction


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


async def CartMenu(chat_id: int) -> ClientMenu:
    order_srv = await ClientOrderService.Create(chat_id)
    order = await order_srv.GetOrder()

    text = order.GetClientInfo() + ClientPosition.Cart()
    buttons = [
        [CreateButton(cb=CartCallbackData, action=CartAction.Pay)],
        [
            CreateButton(cb=CartCallbackData, action=CartAction.Change),
            CreateButton(cb=CartCallbackData, action=CartAction.Clean),
        ],
        [CreateButton(cb=CartCallbackData, action=CartAction.InHub)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetClientHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
