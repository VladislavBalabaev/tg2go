from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.hub import HubMenu
from tg2go.bot.handlers.client.menus.panel import (
    BackToPanelReplyMarkup,
    PanelAction,
    PanelCallbackData,
    PanelMenu,
)

router = Router()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Menu))
async def PanelHub(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await HubMenu(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Address))
async def PanelAddress(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_text(
        text="Адрес такой-то",  # TODO
        reply_markup=BackToPanelReplyMarkup(),
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.About))
async def PanelAbout(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_text(
        text="Мы те-то",  # TODO
        reply_markup=BackToPanelReplyMarkup(),
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.AboutService))
async def PanelAboutService(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_text(
        text="Сервис вот, пишите @vbalab",  # TODO
        reply_markup=BackToPanelReplyMarkup(),
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Back))
async def PanelBack(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = PanelMenu()

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
