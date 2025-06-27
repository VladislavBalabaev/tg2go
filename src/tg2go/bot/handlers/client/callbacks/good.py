from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.cart.cart import CartMenu
from tg2go.bot.handlers.client.menus.category import CategoryMenu
from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.good import GoodAction, GoodCallbackData
from tg2go.bot.handlers.client.menus.item import ItemMenu
from tg2go.services.client.good import ClientGoodService
from tg2go.services.client.order import ClientOrderService

router = Router()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Cart))
async def GoodCard(callback_query: types.CallbackQuery) -> None:
    new_menu = await CartMenu(callback_query.from_user.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.AddGood))
async def GoodItem(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = await ClientOrderService.Create(callback_query.message.chat.id)
    order_item_id = await srv.AddGoodInOrder(callback_data.good_id)

    new_menu = await ItemMenu(
        chat_id=callback_query.from_user.id,
        order_item_id=order_item_id,
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Back))
async def GoodBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    srv = ClientGoodService.Create()
    good = await srv.GetGood(callback_data.good_id)

    new_menu = await CategoryMenu(
        chat_id=callback_query.from_user.id,
        category_id=good.category_id,
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
