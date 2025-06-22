from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.card import CardMenu
from tg2go.bot.handlers.client.menus.category import CategoryMenu
from tg2go.bot.handlers.client.menus.good import GoodAction, GoodCallbackData
from tg2go.bot.handlers.client.menus.item import ItemMenu
from tg2go.services.client.good import ClientGoodService
from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Card))
async def GoodCard(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CardMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.AddGood))
async def GoodItem(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.from_user.id)
    order_item_id = await srv.AddGoodInOrder(callback_data.good_id)

    menu = await ItemMenu(
        chat_id=callback_query.from_user.id,
        order_item_id=order_item_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Back))
async def GoodBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = ClientGoodService.Create()
    good = await srv.GetGood(callback_data.good_id)

    menu = await CategoryMenu(
        chat_id=callback_query.from_user.id,
        category_id=good.category_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
