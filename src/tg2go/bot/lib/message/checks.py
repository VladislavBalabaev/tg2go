from tg2go.db.models.clients import TgUser
from tg2go.db.services.user_context import GetUserContextService


async def CheckVerified(chat_id: int) -> bool:
    ctx = await GetUserContextService()

    verified = await ctx.GetTgUser(
        chat_id=chat_id,
        column=TgUser.verified,
    )

    return verified if verified else False
