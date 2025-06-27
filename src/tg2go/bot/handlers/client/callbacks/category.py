from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import CartMenu
from tg2go.bot.handlers.client.menus.category import (
    CategoryAction,
    CategoryCallbackData,
    CategoryGoodCallbackData,
)
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.good import GoodMenu
from tg2go.bot.handlers.client.menus.hub import HubMenu

router = Router()


@router.callback_query(CategoryCallbackData.filter(F.action == CategoryAction.Cart))
async def CategoryCard(callback_query: types.CallbackQuery) -> None:
    new_menu = await CartMenu(callback_query.from_user.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CategoryGoodCallbackData.filter())
async def CategoryGood(
    callback_query: types.CallbackQuery,
    callback_data: CategoryGoodCallbackData,
) -> None:
    new_menu = await GoodMenu(callback_data.good_id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(CategoryCallbackData.filter(F.action == CategoryAction.Back))
async def CategoryBack(callback_query: types.CallbackQuery) -> None:
    new_menu = await HubMenu(callback_query.from_user.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
