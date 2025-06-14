import logging

from tg2go.bot.lib.chat.username import GetChatUserLoggingPart
from tg2go.db.models.clients import TgUser
from tg2go.db.services.user_context import GetUserContextService
from tg2go.recsys.searching.document import DeleteUserOpenSearch


async def CheckIfBlocked(chat_id: int) -> bool:
    ctx = await GetUserContextService()
    blocked = await ctx.GetTgUser(chat_id=chat_id, column=TgUser.blocked)

    if blocked:
        part = await GetChatUserLoggingPart(chat_id)
        logging.info(f"{part} messages while being blocked.")

    return blocked or False


async def _UnverifyUser(chat_id: int) -> None:
    ctx = await GetUserContextService()

    await ctx.UpdateTgUser(
        chat_id=chat_id,
        column=TgUser.verified,
        value=False,
    )

    nes_id = await ctx.GetTgUser(chat_id=chat_id, column=TgUser.nes_id)
    if nes_id:
        await DeleteUserOpenSearch(nes_id)

    logging.info(f"chat_id={chat_id} unverified.")


async def BlockUser(chat_id: int) -> None:
    ctx = await GetUserContextService()

    await ctx.UpdateTgUser(
        chat_id=chat_id,
        column=TgUser.blocked,
        value=True,
    )

    await _UnverifyUser(chat_id)

    part = await GetChatUserLoggingPart(chat_id)
    logging.info(f"{part} blocked.")


async def UnblockUser(chat_id: int) -> None:
    ctx = await GetUserContextService()

    await ctx.UpdateTgUser(
        chat_id=chat_id,
        column=TgUser.blocked,
        value=False,
    )

    part = await GetChatUserLoggingPart(chat_id)
    logging.info(f"{part} unblocked.")


async def UserBlockedBot(chat_id: int) -> None:
    await _UnverifyUser(chat_id)

    logging.info(f"chat_id={chat_id} blocked the bot.")
