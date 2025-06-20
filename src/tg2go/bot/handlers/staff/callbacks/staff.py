from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.settings import SettingsMenu
from tg2go.bot.handlers.staff.menus.staff import (
    StaffAction,
    StaffCallbackData,
    StaffMenu,
)
from tg2go.bot.lifecycle.active import bot_state

router = Router()


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.Activate))
async def StaffActivate(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    bot_state.Activate()

    menu = StaffMenu(callback_query.message.chat.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.Deactivate))
async def StaffDeactivate(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    bot_state.Deactivate()

    menu = StaffMenu(callback_query.message.chat.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.Settings))
async def StaffSettings(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await SettingsMenu(callback_query.message.chat.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.Cancel))
async def StaffCancel(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()
