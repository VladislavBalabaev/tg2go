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


def IsInactiveBot(chat_id: int) -> bool:
    if chat_id in STAFF_CHAT_IDS or chat_id in ADMIN_CHAT_IDS:
        return True

    return bot_state.active


class MessageLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        if await CheckIfBlocked(event.chat.id):
            return

        await ReceiveMessage(event)

        if IsInactiveBot(event.chat.id):
            await SendMessage(
                chat_id=event.chat.id,
                text="Бот не активен.",
            )
            return

        return await handler(event, data)


class CallbackLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        if await CheckIfBlocked(event.from_user.id):
            return

        callback_data = data.get("callback_data")
        assert isinstance(callback_data, CallbackData)

        await ReceiveCallback(
            query=event,
            data=callback_data,
        )

        if IsInactiveBot(event.from_user.id):
            await SendMessage(
                chat_id=event.chat.id,
                text="Бот не активен.",
            )
            return

        return await handler(event, data)


def SetBotMiddleware(dp: Dispatcher) -> None:
    dp.message.middleware(MessageLoggingMiddleware())
    dp.callback_query.middleware(CallbackLoggingMiddleware())
