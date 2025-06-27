from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import CartMenu
from tg2go.bot.handlers.client.menus.cart.items import (
    CartItemsAction,
    CartItemsCallbackData,
    CartItemsItemCallbackData,
)
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.item import ItemMenu

router = Router()


@router.callback_query(CartItemsItemCallbackData.filter())
async def CartItemsItem(
    callback_query: types.CallbackQuery,
    callback_data: CartItemsItemCallbackData,
) -> None:
    new_menu = await ItemMenu(
        chat_id=callback_query.from_user.id,
        order_item_id=callback_data.order_item_id,
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CartItemsCallbackData.filter(F.action == CartItemsAction.Back))
async def CartItemsBack(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await CartMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
