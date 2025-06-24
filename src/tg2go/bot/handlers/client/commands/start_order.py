import logging

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.handlers.client.menus.panel import PanelMenu
from tg2go.bot.lib.message.filter import HasOrderFilter, VerifiedFilter
from tg2go.bot.lib.message.io import SendMessage
from tg2go.services.client.order import ClientOrderService, CreateNewOrder

router = Router()


async def SendPanelMenu(message: types.Message) -> None:
    menu = PanelMenu()

    msg = await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    if msg is None:
        logging.error(f"Can't send order to chat_id={message.chat.id}")
        return

    srv = await ClientOrderService.Create(message.chat.id)
    await srv.SetOrderMessage(msg.message_id)


@router.message(StateFilter(None), Command("start"), VerifiedFilter(), HasOrderFilter())
async def CommandStartRestart(message: types.Message) -> None:
    srv = await ClientOrderService.Create(message.chat.id)
    await srv.DeleteOrderMessage()

    await SendPanelMenu(message)


@router.message(StateFilter(None), Command("start"), VerifiedFilter())
async def CommandStartNew(message: types.Message) -> None:
    await CreateNewOrder(message.chat.id)

    await SendPanelMenu(message)
