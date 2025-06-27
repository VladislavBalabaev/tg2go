from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
)
from tg2go.bot.lib.message.image import GetGoodImageDir
from tg2go.db.models.common.types import OrderItemId
from tg2go.services.client.order import ClientOrderService


class ItemAction(ClientAction):
    Cart = "🛒 Корзина"
    Add = "➕ Добавить"
    Reduce = "➖ Убрать"
    Back = "⬅️ Назад"


class ItemCallbackData(CallbackData, prefix="client.item"):
    action: ItemAction
    order_item_id: OrderItemId


def CreateButton(
    action: ClientAction, order_item_id: OrderItemId
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=ItemCallbackData(
            action=action,
            order_item_id=order_item_id,
        ).pack(),
    )


async def ItemMenu(chat_id: int, order_item_id: OrderItemId) -> ClientMenu:
    srv = await ClientOrderService.Create(chat_id)
    order_item = await srv.GetOrderItem(order_item_id)

    text = order_item.GetClientInfo() + ClientPosition.Item(order_item)
    buttons = [
        [
            CreateButton(
                action=ItemAction.Cart,
                order_item_id=order_item_id,
            )
        ],
        [
            CreateButton(
                action=ItemAction.Reduce,
                order_item_id=order_item_id,
            ),
            CreateButton(
                action=ItemAction.Add,
                order_item_id=order_item_id,
            ),
        ],
        [
            CreateButton(
                action=ItemAction.Back,
                order_item_id=order_item_id,
            )
        ],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetGoodImageDir(order_item.good_id),
        caption=text,
        reply_markup=markup,
    )
