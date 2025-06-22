from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.card import CardAction, CardCallbackData
from tg2go.bot.handlers.client.menus.hub import HubMenu

# from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(CardCallbackData.filter(F.action == CardAction.Pay))
async def CardPay(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    # TODO make payment system
    menu = await HubMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(CardCallbackData.filter(F.action == CardAction.InHub))
async def CardInHub(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await HubMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
