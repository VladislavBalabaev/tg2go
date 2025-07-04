from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
    SplitButtonsInTwoColumns,
)
from tg2go.bot.lib.message.image import GetClientHeaderDir
from tg2go.db.models.common.types import OrderItemId
from tg2go.services.client.order import ClientOrderService


class CartItemsAction(ClientAction):
    Back = "⬅️ Назад"


class CartItemsCallbackData(CallbackData, prefix="client.items"):
    action: CartItemsAction


class CartItemsItemCallbackData(CallbackData, prefix="client.items.item"):
    order_item_id: OrderItemId


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


async def CartItemsMenu(chat_id: int) -> ClientMenu:
    order_srv = await ClientOrderService.Create(chat_id)
    order = await order_srv.GetOrder()

    text = order.GetClientInfo() + ClientPosition.Cart()

    plain_buttons = [
        InlineKeyboardButton(
            text=item.good.name,
            callback_data=CartItemsItemCallbackData(
                order_item_id=item.order_item_id
            ).pack(),
        )
        for item in order.order_items
    ]

    buttons = [
        *SplitButtonsInTwoColumns(plain_buttons),
        [CreateButton(cb=CartItemsCallbackData, action=CartItemsAction.Back)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetClientHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
