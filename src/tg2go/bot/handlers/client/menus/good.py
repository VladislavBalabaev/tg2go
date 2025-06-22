from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.client.menus.common import ClientAction, ClientPosition, Menu
from tg2go.db.models.common.types import GoodId
from tg2go.services.client.good import ClientGoodService


class GoodAction(ClientAction):
    Card = "🛒 Корзина"
    AddGood = "➕ Добавить в корзину"
    Back = "⬅️ Назад"


class GoodCallbackData(CallbackData, prefix="client.good"):
    action: GoodAction
    good_id: GoodId


def CreateButton(action: ClientAction, good_id: GoodId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=GoodCallbackData(
            action=action,
            good_id=good_id,
        ).pack(),
    )


async def GoodMenu(good_id: GoodId) -> Menu:
    srv = ClientGoodService.Create()
    good = await srv.GetGood(good_id)

    text = good.GetInfoForClient() + ClientPosition.Good(good)
    buttons = [
        [CreateButton(action=GoodAction.Card, good_id=good_id)],
        [CreateButton(action=GoodAction.AddGood, good_id=good_id)],
        [CreateButton(action=GoodAction.Back, good_id=good_id)],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return Menu(
        text=text,
        reply_markup=markup,
    )
