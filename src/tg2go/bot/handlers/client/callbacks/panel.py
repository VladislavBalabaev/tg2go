from aiogram import F, Router, types

from tg2go.bot.handlers.client.menus.common import ChangeToNewClientMenu
from tg2go.bot.handlers.client.menus.hub import HubMenu
from tg2go.bot.handlers.client.menus.panel import (
    PanelAction,
    PanelCallbackData,
    PanelMenu,
    PanelMenuExplain,
)

router = Router()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Menu))
async def PanelHub(callback_query: types.CallbackQuery) -> None:
    new_menu = await HubMenu(callback_query.from_user.id)

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.About))
async def PanelAbout(callback_query: types.CallbackQuery) -> None:
    new_menu = PanelMenuExplain(
        text="Круглосуточная шаурма на Толбухина 13А с 4.8⭐️ на Яндексе!"
    )  # TODO

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.AboutService))
async def PanelAboutService(callback_query: types.CallbackQuery) -> None:
    new_menu = PanelMenuExplain(
        text="<b>tg2go</b> - сервис быстрых заказов через Telegram для уличной еды.\n\nПо вопросам и предложениям, пожалуйста, пишите @vbalab 😊"
    )

    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()


@router.callback_query(PanelCallbackData.filter(F.action == PanelAction.Back))
async def PanelBack(callback_query: types.CallbackQuery) -> None:
    new_menu = PanelMenu()
    await ChangeToNewClientMenu(
        callback_query=callback_query,
        new_menu=new_menu,
    )
    await callback_query.answer()
