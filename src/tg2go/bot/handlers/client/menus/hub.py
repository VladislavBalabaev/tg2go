from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import (
    ClientAction,
    ClientMenu,
    ClientPosition,
)
from tg2go.bot.lib.message.image import GetHeaderDir
from tg2go.db.models.common.types import CategoryId
from tg2go.services.client.category import ClientCategoryService
from tg2go.services.client.order import ClientOrderService


class HubAction(ClientAction):
    Card = "🛒 Корзина"
    Back = "⬅️ Назад"


class HubCallbackData(CallbackData, prefix="client.hub"):
    action: HubAction


class HubCategoryCallbackData(CallbackData, prefix="client.hub.cat"):
    category_id: CategoryId


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )


async def HubMenu(chat_id: int) -> ClientMenu:
    order_srv = await ClientOrderService.Create(chat_id)
    order = await order_srv.GetOrder()

    cat_srv = ClientCategoryService.Create()
    categories = await cat_srv.GetSortedCategories()

    buttons = []

    group = []
    for i, cat in enumerate(categories):
        group.append(
            InlineKeyboardButton(
                text=cat.name,
                callback_data=HubCategoryCallbackData(
                    category_id=cat.category_id
                ).pack(),
            )
        )

        if i % 2 == 1:
            buttons.append(group)
            group = []

    if group:
        buttons.append(group)

    text = order.GetClientInfo() + ClientPosition.Hub()
    buttons = [
        [CreateButton(cb=HubCallbackData, action=HubAction.Card)],
        *buttons,
        [CreateButton(cb=HubCallbackData, action=HubAction.Back)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ClientMenu(
        image_dir=GetHeaderDir(),
        caption=text,
        reply_markup=markup,
    )
