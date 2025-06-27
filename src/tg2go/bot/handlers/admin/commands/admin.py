from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.lib.message.filter import AdminFilter
from tg2go.bot.lib.message.io import SendMessage

router = Router()

_commands = """/logs
Посмотреть логи

/send
Отправить сообщение пользователю

/senda
Разослать сообщение всем подтверждённым пользователям

/blocking
Статус блокировки пользователя
"""


@router.message(Command("admin"), StateFilter(None), AdminFilter())
async def CommandAdmin(message: types.Message) -> None:
    await SendMessage(chat_id=message.chat.id, text=_commands)
