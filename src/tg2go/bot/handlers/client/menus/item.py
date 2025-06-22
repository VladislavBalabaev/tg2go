from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import ClientAction, Menu
from tg2go.db.models.common.types import OrderItemId
from tg2go.services.client.order import ClientOrderService


class ItemAction(ClientAction):
    AddItem = "➕ Добавить"
    ReduceItem = "➖ Убрать"
    Back = "⬅️ Назад"


class ItemCallbackData(CallbackData, prefix="client.good"):
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


async def ItemMenu(chat_id: int, order_item_id: OrderItemId) -> Menu:
    srv = await ClientOrderService.Create(chat_id)

    text = await srv.GetOrderItemInfo(order_item_id)
    buttons = [
        [
            CreateButton(
                action=ItemAction.AddItem,
                order_item_id=order_item_id,
            ),
            CreateButton(
                action=ItemAction.ReduceItem,
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

    return Menu(
        text=text,
        reply_markup=markup,
    )
