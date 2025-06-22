from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.card import CardMenu
from tg2go.bot.handlers.client.menus.category import CategoryMenu
from tg2go.bot.handlers.client.menus.good import GoodMenu
from tg2go.bot.handlers.client.menus.item import ItemAction, ItemCallbackData, ItemMenu
from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Card))
async def ItemCard(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CardMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Add))
async def ItemAdd(
    callback_query: types.CallbackQuery,
    callback_data: ItemCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.from_user.id)
    item = await srv.GetOrderItem(callback_data.order_item_id)
    order_item_id = await srv.AddGoodInOrder(item.good.good_id)

    menu = await ItemMenu(
        chat_id=callback_query.from_user.id,
        order_item_id=order_item_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Reduce))
async def ItemReduce(
    callback_query: types.CallbackQuery,
    callback_data: ItemCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.from_user.id)
    item = await srv.GetOrderItem(callback_data.order_item_id)  # mb not working
    quanitity_before = item.quantity
    order_item_id = await srv.ReduceGoodInOrder(item.good.good_id)

    if quanitity_before == 1:
        menu = await GoodMenu(item.good.good_id)
    else:
        menu = await ItemMenu(
            chat_id=callback_query.from_user.id,
            order_item_id=order_item_id,
        )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Back))
async def ItemBack(
    callback_query: types.CallbackQuery,
    callback_data: ItemCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.from_user.id)
    item = await srv.GetOrderItem(callback_data.order_item_id)

    menu = await CategoryMenu(
        chat_id=callback_query.from_user.id,
        category_id=item.good.category_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
