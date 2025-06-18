# import logging

from aiogram import Router, types

# from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from tg2go.bot.lib.chat.username import GetChatUserLoggingPart
from tg2go.bot.lib.message.filters import HasOrderFilter, VerifiedFilter
from tg2go.services.client.order import CreateNewOrder, GetOrderService

router = Router()


@router.message(StateFilter(None), Command("start"), VerifiedFilter(), HasOrderFilter())
async def CommandStartRestart(message: types.Message) -> None:
    srv = await GetOrderService(message.chat.id)

    await srv.DeleteOrderMessage()
    await srv.DeleteGoodMessage()

    text = await srv.OrderInfo()

    # send new message and save it to order


@router.message(StateFilter(None), Command("start"), VerifiedFilter())
async def CommandStartNew(message: types.Message) -> None:
    await CreateNewOrder(message.chat.id)

    srv = await GetOrderService(message.chat.id)

    # send new message and save it to order
