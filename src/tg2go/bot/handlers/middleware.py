from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message

from tg2go.bot.lib.chat.block import CheckIfBlocked
from tg2go.bot.lib.message.io import (
    ReceiveCallback,
    ReceiveMessage,
    SendMessage,
)
from tg2go.bot.lifecycle.active import bot_state
from tg2go.core.configs.constants import ADMIN_CHAT_IDS, STAFF_CHAT_IDS

_IDS = [*ADMIN_CHAT_IDS, *STAFF_CHAT_IDS]


class MessageLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        message: Message,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        if await CheckIfBlocked(message.chat.id):
            return

        await ReceiveMessage(message)

        if not bot_state.active and message.chat.id not in _IDS:
            await SendMessage(
                chat_id=message.chat.id,
                text="Бот не активен.",
            )
            return

        return await handler(message, data)


class CallbackLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        callback_query: CallbackQuery,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        assert isinstance(callback_query.message, Message)

        if await CheckIfBlocked(callback_query.message.chat.id):
            return

        callback_data = data.get("callback_data")
        assert isinstance(callback_data, CallbackData)

        await ReceiveCallback(
            query=callback_query,
            data=callback_data,
        )

        if not bot_state.active and "client" in callback_data.__prefix__:
            await SendMessage(
                chat_id=callback_query.message.chat.id,
                text="Бот не активен.",
            )
            return

        return await handler(callback_query, data)


def SetBotMiddleware(dp: Dispatcher) -> None:
    dp.message.middleware(MessageLoggingMiddleware())
    dp.callback_query.middleware(CallbackLoggingMiddleware())
