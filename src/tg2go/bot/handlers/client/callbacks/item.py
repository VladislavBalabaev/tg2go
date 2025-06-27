from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import CartMenu
from tg2go.bot.handlers.client.menus.category import CategoryMenu
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.good import GoodMenu
from tg2go.bot.handlers.client.menus.item import ItemAction, ItemCallbackData, ItemMenu
from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Cart))
async def ItemCard(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    new_menu = await CartMenu(callback_query.message.chat.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Add))
async def ItemAdd(
    callback_query: types.CallbackQuery,
    callback_data: ItemCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.message.chat.id)
    item = await srv.GetOrderItem(callback_data.order_item_id)
    order_item_id = await srv.AddGoodInOrder(item.good.good_id)

    new_menu = await ItemMenu(
        chat_id=callback_query.message.chat.id,
        order_item_id=order_item_id,
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Reduce))
async def ItemReduce(
    callback_query: types.CallbackQuery,
    callback_data: ItemCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.message.chat.id)
    item = await srv.GetOrderItem(callback_data.order_item_id)  # mb not working

    quanitity_before = item.quantity
    order_item_id = await srv.ReduceGoodInOrder(item.good.good_id)

    if quanitity_before == 1:
        new_menu = await GoodMenu(item.good.good_id)
    else:
        new_menu = await ItemMenu(
            chat_id=callback_query.message.chat.id,
            order_item_id=order_item_id,
        )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(ItemCallbackData.filter(F.action == ItemAction.Back))
async def ItemBack(
    callback_query: types.CallbackQuery,
    callback_data: ItemCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.message.chat.id)
    item = await srv.GetOrderItem(callback_data.order_item_id)

    new_menu = await CategoryMenu(
        chat_id=callback_query.message.chat.id,
        category_id=item.good.category_id,
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
