from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.card import CardMenu
from tg2go.bot.handlers.client.menus.category import CategoryMenu
from tg2go.bot.handlers.client.menus.hub import (
    HubAction,
    HubCallbackData,
    HubCategoryCallbackData,
)
from tg2go.bot.handlers.client.menus.panel import PanelMenu

router = Router()


@router.callback_query(HubCallbackData.filter(F.action == HubAction.Card))
async def HubCard(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CardMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(HubCategoryCallbackData.filter())
async def HubCategory(
    callback_query: types.CallbackQuery,
    callback_data: HubCategoryCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CategoryMenu(
        chat_id=callback_query.from_user.id,
        category_id=callback_data.category_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(HubCallbackData.filter(F.action == HubAction.Back))
async def HubBack(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = PanelMenu()

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
