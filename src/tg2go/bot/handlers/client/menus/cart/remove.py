from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
from tg2go.services.client.order import ClientOrderService


class CartRemoveAction(ClientAction):
    Delete = "🗑️ Точно очистить"
    Back = "⬅️ Назад"


class CartRemoveCallbackData(CallbackData, prefix="staff.cat.remove"):
    action: CartRemoveAction


def CreateButton(action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=CartRemoveCallbackData(action=action).pack(),
    )


async def CartRemoveMenu(chat_id: int) -> ClientMenu:
    order_srv = await ClientOrderService.Create(chat_id)
    order = await order_srv.GetOrder()

    text = order.GetClientInfo() + ClientPosition.Cart()

    buttons = [
        [CreateButton(action=CartRemoveAction.Delete)],
        [CreateButton(action=CartRemoveAction.Back)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
