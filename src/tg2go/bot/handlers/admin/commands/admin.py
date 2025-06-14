from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.lib.message.filters import AdminFilter
from tg2go.bot.lib.message.io import SendMessage

router = Router()

_commands = """/logs
See logs

/messages
See messages of a user

/send
Send message to a user

/senda
Send messages to all verified users

/blocking
State whether user block or not
"""


@router.message(Command("admin"), StateFilter(None), AdminFilter())
async def CommandAdmin(message: types.Message) -> None:
    await SendMessage(chat_id=message.chat.id, text=_commands)
