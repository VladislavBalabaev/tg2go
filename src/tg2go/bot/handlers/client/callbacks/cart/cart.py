from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import (
    CartAction,
    CartCallbackData,
)
from tg2go.bot.handlers.client.menus.cart.items import CartItemsMenu
from tg2go.bot.handlers.client.menus.cart.remove import CartRemoveMenu
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.hub import HubMenu

# from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(CartCallbackData.filter(F.action == CartAction.Pay))
async def CartPay(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    # TODO make payment system
    new_menu = await HubMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CartCallbackData.filter(F.action == CartAction.Change))
async def CartChange(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await CartItemsMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CartCallbackData.filter(F.action == CartAction.Clean))
async def CartClean(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await CartRemoveMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CartCallbackData.filter(F.action == CartAction.InHub))
async def CartInHub(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await HubMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
