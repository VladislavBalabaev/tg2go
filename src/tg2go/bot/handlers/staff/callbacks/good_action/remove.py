from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.good import GoodMenu
from tg2go.bot.handlers.staff.menus.good_action.remove import (
    GoodRemoveAction,
    GoodRemoveCallbackData,
)
from tg2go.bot.lib.message.io import SendMessage
from tg2go.services.staff.good import StaffGoodService

router = Router()


@router.callback_query(
    GoodRemoveCallbackData.filter(F.action == GoodRemoveAction.Delete)
)
async def GoodRemoveDelete(
    callback_query: types.CallbackQuery,
    callback_data: GoodRemoveCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    srv = StaffGoodService.Create()
    await srv.InvalidateGood(callback_data.good_id)

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Позиция успешно удалена",
    )

    good = await srv.GetGood(callback_data.good_id)

    menu = await CategoryMenu(good.category_id)
    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await callback_query.message.delete()
    await callback_query.answer()


@router.callback_query(GoodRemoveCallbackData.filter(F.action == GoodRemoveAction.Back))
async def GoodRemoveBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodRemoveCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await GoodMenu(callback_data.good_id)

    await callback_query.message.edit_media(
        media=menu.media,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
