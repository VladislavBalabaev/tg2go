# import logging

from aiogram import Router, types

# from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from tg2go.bot.lib.chat.username import GetChatUserLoggingPart
# from tg2go.bot.lib.message.io import SendMessage
from tg2go.bot.lib.message.filters import HasOrderFilter, VerifiedFilter
from tg2go.services.client.order import ClientOrderService, CreateNewOrder

router = Router()


@router.message(StateFilter(None), Command("start"), VerifiedFilter(), HasOrderFilter())
async def CommandStartRestart(message: types.Message) -> None:
    srv = await ClientOrderService.Create(message.chat.id)

    await srv.DeleteOrderMessage()
    await srv.DeleteGoodMessage()

    text = await srv.GetOrderInfo()

    # send new message and save it to order


@router.message(StateFilter(None), Command("start"), VerifiedFilter())
async def CommandStartNew(message: types.Message) -> None:
    await CreateNewOrder(message.chat.id)

    srv = await ClientOrderService.Create(message.chat.id)

    # msg = await SendMessage(chat_id=message.chat.id, text=..., reply_markup=...)
    # await ....UpdateOrder(order_id, Order.order_message_id, msg.message_id)

    # send new message and save it to order
