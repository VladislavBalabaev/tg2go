from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import ClientAction, Menu
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.services.client.good import ClientGoodService
from tg2go.services.client.order import ClientOrderService


class CategoryAction(ClientAction):
    Back = "⬅️ Назад"


class CategoryCallbackData(CallbackData, prefix="client.cat"):
    action: CategoryAction
    category_id: CategoryId


class CategoryGoodCallbackData(CallbackData, prefix="client.cat.good"):
    category_id: CategoryId
    good_id: GoodId


def CreateButton(action: ClientAction, category_id: CategoryId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=CategoryCallbackData(
            action=action, category_id=category_id
        ).pack(),
    )


async def CategoryMenu(chat_id: int, category_id: CategoryId) -> Menu:
    order_srv = await ClientOrderService.Create(chat_id)

    good_srv = ClientGoodService.Create()
    goods = await good_srv.GetAvailableGoods(category_id)

    buttons = []

    group = []
    for i, good in enumerate(goods):
        group.append(
            InlineKeyboardButton(
                text=good.name,
                callback_data=CategoryGoodCallbackData(
                    category_id=category_id,
                    good_id=good.good_id,
                ).pack(),
            )
        )

        if i % 2 == 1:
            buttons.append(group)
            group = []

    if group:
        buttons.append(group)

    text = await order_srv.GetOrderInfo()
    buttons = [
        *buttons,
        [CreateButton(action=CategoryAction.Back, category_id=category_id)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
