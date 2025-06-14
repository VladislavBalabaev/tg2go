from aiogram import Router, types
from aiogram.filters.command import Command

from tg2go.bot.lib.message.filters import AdminFilter
from tg2go.bot.lib.message.io import SendDocument
from tg2go.core.configs.paths import PATH_BOT_LOGS

router = Router()


@router.message(Command("logs"), AdminFilter())
async def CommandLogs(message: types.Message) -> None:
    await SendDocument(
        chat_id=message.chat.id, document=types.FSInputFile(PATH_BOT_LOGS)
    )
