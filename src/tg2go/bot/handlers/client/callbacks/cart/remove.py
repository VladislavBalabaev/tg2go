from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import CartMenu
from tg2go.bot.handlers.client.menus.cart.remove import (
    CartRemoveAction,
    CartRemoveCallbackData,
)
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.hub import HubMenu
from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(
    CartRemoveCallbackData.filter(F.action == CartRemoveAction.Delete)
)
async def CategoryRemoveDelete(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.message.chat.id)
    await srv.ClearOrder()

    new_menu = await HubMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CartRemoveCallbackData.filter(F.action == CartRemoveAction.Back))
async def CategoryRemoveBack(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await CartMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
