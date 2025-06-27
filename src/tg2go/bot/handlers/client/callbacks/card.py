from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.card import CardAction, CardCallbackData
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.hub import HubMenu

# from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(CardCallbackData.filter(F.action == CardAction.Pay))
async def CardPay(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    # TODO make payment system
    new_menu = await HubMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CardCallbackData.filter(F.action == CardAction.InHub))
async def CardInHub(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await HubMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
