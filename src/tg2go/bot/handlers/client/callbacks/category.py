from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.card import CardMenu
from tg2go.bot.handlers.client.menus.category import (
    CategoryAction,
    CategoryCallbackData,
    CategoryGoodCallbackData,
)
from tg2go.bot.handlers.client.menus.good import GoodMenu
from tg2go.bot.handlers.client.menus.hub import HubMenu

router = Router()


@router.callback_query(CategoryCallbackData.filter(F.action == CategoryAction.Card))
async def CategoryCard(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CardMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(CategoryGoodCallbackData.filter())
async def CategoryGood(
    callback_query: types.CallbackQuery,
    callback_data: CategoryGoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await GoodMenu(callback_data.good_id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(CategoryCallbackData.filter(F.action == CategoryAction.Back))
async def CategoryBack(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await HubMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
