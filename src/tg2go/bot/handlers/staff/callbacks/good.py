from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.good import GoodAction, GoodCallbackData
from tg2go.bot.handlers.staff.menus.good_action.change import GoodChangeMenu
from tg2go.bot.handlers.staff.menus.good_action.remove import GoodRemoveMenu
from tg2go.bot.lib.message.io import SendMessage
from tg2go.services.staff.good import StaffGoodService

router = Router()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.ChangeGood))
async def GoodChangeGood(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await GoodChangeMenu(callback_data.good_id)

    await callback_query.message.edit_media(
        media=menu.media,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.RemoveGood))
async def GoodRemoveGood(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await GoodRemoveMenu(callback_data.good_id)

    await callback_query.message.edit_media(
        media=menu.media,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Back))
async def CategoryBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    srv = StaffGoodService.Create()
    good = await srv.GetGood(callback_data.good_id)

    menu = await CategoryMenu(good.category_id)
    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await callback_query.message.delete()
