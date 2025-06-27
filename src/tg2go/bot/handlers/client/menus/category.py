from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
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


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


async def CategoryMenu(chat_id: int, category_id: CategoryId) -> ClientMenu:
    order_srv = await ClientOrderService.Create(chat_id)
    order = await order_srv.GetOrder()
    cat_srv = ClientCategoryService.Create()
    category = await cat_srv.GetCategory(category_id)

    text = order.GetClientInfo() + ClientPosition.Category(category)

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

    buttons = [
        [CreateButton(cb=CategoryCallbackData, action=CategoryAction.Card)],
        *buttons,
        [CreateButton(cb=CategoryCallbackData, action=CategoryAction.Back)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
