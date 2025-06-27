from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.category.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.common import menu
from tg2go.bot.handlers.staff.menus.good.change import GoodChangeMenu
from tg2go.bot.handlers.staff.menus.good.good import GoodAction, GoodCallbackData
from tg2go.bot.handlers.staff.menus.good.remove import GoodRemoveMenu
from tg2go.services.staff.good import StaffGoodService

router = Router()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.ChangeGood))
async def GoodChangeGood(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    await menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await GoodChangeMenu(callback_data.good_id),
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.RemoveGood))
async def GoodRemoveGood(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    await menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await GoodRemoveMenu(callback_data.good_id),
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Back))
async def GoodBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = StaffGoodService.Create()
    good = await srv.GetGood(callback_data.good_id)

    await menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await CategoryMenu(good.category_id),
    )
    await callback_query.answer()
