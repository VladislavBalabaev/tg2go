from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import ClientAction, ClientPosition, Menu
from tg2go.db.models.common.types import OrderItemId
from tg2go.services.client.order import ClientOrderService


class ItemAction(ClientAction):
    Card = "🛒 Корзина"
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


async def ItemMenu(chat_id: int, order_item_id: OrderItemId) -> Menu:
    srv = await ClientOrderService.Create(chat_id)
    order_item = await srv.GetOrderItem(order_item_id)

    text = order_item.GetInfoForClient() + ClientPosition.Item(order_item)
    buttons = [
        [
            CreateButton(
                action=ItemAction.Card,
                order_item_id=order_item_id,
            )
        ],
        [
            CreateButton(
                action=ItemAction.Add,
                order_item_id=order_item_id,
            ),
            CreateButton(
                action=ItemAction.Reduce,
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
