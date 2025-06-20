
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from tg2go.bot.handlers.staff.callbacks.good_action.add import AddGoodStates
from tg2go.bot.handlers.staff.menus.category import (
    CategoryAction,
    CategoryCallbackData,
    CategoryGoodCallbackData,
)
from tg2go.bot.handlers.staff.menus.good import GoodMenu
from tg2go.bot.handlers.staff.menus.settings import SettingsMenu
from tg2go.bot.lib.message.io import SendMessage

router = Router()


@router.callback_query(CategoryCallbackData.filter(F.action == CategoryAction.AddGood))
async def CategoryAddGood(
    callback_query: types.CallbackQuery,
    callback_data: CategoryCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите название нового продукта",
    )

    await state.set_state(AddGoodStates.name)


@router.callback_query(
    CategoryCallbackData.filter(F.action == CategoryAction.ChangeCategory)
)
async def CategoryChangeCategory(
    callback_query: types.CallbackQuery,
    callback_data: CategoryCallbackData,
    state: FSMContext,
) -> None: ...


@router.callback_query(
    CategoryCallbackData.filter(F.action == CategoryAction.RemoveCategory)
)
async def CategoryRemoveCategory(
    callback_query: types.CallbackQuery,
    callback_data: CategoryCallbackData,
    state: FSMContext,
) -> None: ...


@router.callback_query(CategoryGoodCallbackData.filter())
async def CategoryGood(
    callback_query: types.CallbackQuery,
    callback_data: CategoryGoodCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await GoodMenu(
        chat_id=callback_query.message.chat.id,
        category_id=callback_data.category_id,
        good_id=callback_data.good_id,
    )

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(CategoryCallbackData.filter(F.action == CategoryAction.Back))
async def CategoryBack(
    callback_query: types.CallbackQuery,
    callback_data: CategoryCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await SettingsMenu(callback_query.message.chat.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
