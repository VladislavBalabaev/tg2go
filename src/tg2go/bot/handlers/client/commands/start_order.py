from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.handlers.client.menus.common import SendClientMenu
from tg2go.bot.handlers.client.menus.panel import PanelMenu
from tg2go.bot.lib.message.filter import HasOrderFilter, VerifiedFilter
from tg2go.services.client.order import CreateNewOrder

router = Router()


async def SendPanelMenu(message: types.Message) -> None:
    await SendClientMenu(chat_id=message.chat.id, menu=PanelMenu())


@router.message(StateFilter(None), Command("start"), VerifiedFilter(), HasOrderFilter())
async def CommandStartRestart(message: types.Message) -> None:
    await SendPanelMenu(message)


@router.message(StateFilter(None), Command("start"), VerifiedFilter())
async def CommandStartNew(message: types.Message) -> None:
    await CreateNewOrder(message.chat.id)

    await SendPanelMenu(message)
