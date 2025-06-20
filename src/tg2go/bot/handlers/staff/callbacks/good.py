
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.good import GoodAction, GoodCallbackData

router = Router()


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.ChangeGood))
async def GoodChangeGood(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
    state: FSMContext,
) -> None: ...


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.RemoveGood))
async def GoodRemoveGood(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
    state: FSMContext,
) -> None: ...


@router.callback_query(GoodCallbackData.filter(F.action == GoodAction.Back))
async def CategoryBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CategoryMenu(
        chat_id=callback_query.message.chat.id,
        category_id=callback_data.category_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
