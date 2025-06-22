from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientPosition,
    CreateButton,
    Menu,
)
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.services.client.category import ClientCategoryService
from tg2go.services.client.good import ClientGoodService
from tg2go.services.client.order import ClientOrderService


class CategoryAction(ClientAction):
    Card = "🛒 Корзина"
    Back = "⬅️ Назад"


class CategoryCallbackData(CallbackData, prefix="client.cat"):
    action: CategoryAction


class CategoryGoodCallbackData(CallbackData, prefix="client.cat.good"):
    good_id: GoodId


async def CategoryMenu(chat_id: int, category_id: CategoryId) -> Menu:
    order_srv = await ClientOrderService.Create(chat_id)
    cat_srv = ClientCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    good_srv = ClientGoodService.Create()
    goods = await good_srv.GetAvailableGoods(category_id)

    buttons = []

    group = []
    for i, good in enumerate(goods):
        group.append(
            InlineKeyboardButton(
                text=good.name,
                callback_data=CategoryGoodCallbackData(good_id=good.good_id).pack(),
            )
        )

        if i % 2 == 1:
            buttons.append(group)
            group = []

    if group:
        buttons.append(group)

    text = await order_srv.GetOrderInfo() + ClientPosition.Category(category)
    buttons = [
        [CreateButton(cb=CategoryCallbackData, action=CategoryAction.Card)],
        *buttons,
        [CreateButton(cb=CategoryCallbackData, action=CategoryAction.Back)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
