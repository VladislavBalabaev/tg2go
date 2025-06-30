from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.common import staff_menu
from tg2go.bot.handlers.staff.menus.panel import (
    ActivePanelAction,
    ActivePanelCallbackData,
    PanelAction,
    PanelCallbackData,
    PanelMenu,
)
from tg2go.bot.handlers.staff.menus.settings import SettingsMenu
from tg2go.bot.lifecycle.active import bot_state

router = Router()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Activate))
async def PanelActivate(callback_query: types.CallbackQuery) -> None:
    bot_state.Activate()

    await staff_menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=PanelMenu(),
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Settings))
async def PanelSettings(callback_query: types.CallbackQuery) -> None:
    await staff_menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await SettingsMenu(),
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Exit))
async def PanelExit(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()


@router.callback_query(
    ActivePanelCallbackData.filter(F.action == ActivePanelAction.Deactivate)
)
async def ActivePanelDeactivate(callback_query: types.CallbackQuery) -> None:
    bot_state.Deactivate()

    await staff_menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=PanelMenu(),
    )
    await callback_query.answer()


@router.callback_query(
    ActivePanelCallbackData.filter(F.action == ActivePanelAction.Exit)
)
async def ActivePanelExit(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()
