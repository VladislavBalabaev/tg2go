from aiogram import types
from aiogram.filters import Filter

from tg2go.bot.lib.message.checks import CheckVerified
from tg2go.core.configs.constants import ADMIN_CHAT_IDS


class AdminFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id in ADMIN_CHAT_IDS


class VerifiedFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return await CheckVerified(message.chat.id)
