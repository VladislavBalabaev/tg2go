from aiogram import Router, types

# from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tg2go.bot.lib.message.filters import VerifiedFilter
from tg2go.bot.lib.message.io import DeleteMessage
from tg2go.services.order import GetOrderService

router = Router()


async def DeleteCurrentOrder(chat_id: int) -> None:
    ctx = GetOrderService()
    order = await ctx.CancelCurrentOrder(chat_id)

    if order is None:
        return

    if order.good_message_id is not None:
        await DeleteMessage(chat_id=chat_id, message_id=order.good_message_id)
    if order.order_message_id is not None:
        await DeleteMessage(chat_id=chat_id, message_id=order.order_message_id)


async def SendHub() -> None: ...


@router.message(StateFilter(None), Command("start"), VerifiedFilter())
async def CommandStart(message: types.Message, state: FSMContext) -> None: ...


# await SendHub()
