from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import CartMenu
from tg2go.bot.handlers.client.menus.category import CategoryMenu
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.hub import (
    HubAction,
    HubCallbackData,
    HubCategoryCallbackData,
)
from tg2go.bot.handlers.client.menus.panel import PanelMenu

router = Router()


@router.callback_query(HubCallbackData.filter(F.action == HubAction.Cart))
async def HubCard(callback_query: types.CallbackQuery) -> None:
    new_menu = await CartMenu(callback_query.from_user.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(HubCategoryCallbackData.filter())
async def HubCategory(
    callback_query: types.CallbackQuery,
    callback_data: HubCategoryCallbackData,
) -> None:
    new_menu = await CategoryMenu(
        chat_id=callback_query.from_user.id,
        category_id=callback_data.category_id,
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(HubCallbackData.filter(F.action == HubAction.Back))
async def HubBack(callback_query: types.CallbackQuery) -> None:
    new_menu = PanelMenu()

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
