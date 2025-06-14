from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.lib.message.filters import AdminFilter
from tg2go.bot.lib.message.io import PersonalMsg, SendMessage, SendMessagesToGroup
from tg2go.db.services.user_context import GetUserContextService

router = Router()


class SendaStates(StatesGroup):
    Message = State()


@router.message(Command("senda"), StateFilter(None), AdminFilter())
async def CommandSenda(message: types.Message, state: FSMContext) -> None:
    await SendMessage(chat_id=message.chat.id, text="Input text of message")
    await state.set_state(SendaStates.Message)


@router.message(StateFilter(SendaStates.Message), F.content_type == "text")
async def CommandSendaMessage(message: types.Message, state: FSMContext) -> None:
    assert message.text is not None

    ctx = await GetUserContextService()
    chat_ids = await ctx.GetVerifiedTgUsersChatId()

    messages = [PersonalMsg(chat_id=chat_id, text=message.text) for chat_id in chat_ids]
    await SendMessagesToGroup(messages)

    await SendMessage(chat_id=message.chat.id, text="Done")
    await state.clear()
