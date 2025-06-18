from tg2go.db.models.user import User
from tg2go.services.user import GetUserService


async def CheckVerified(chat_id: int) -> bool:
    ctx = GetUserService()

    verified = await ctx.GetUser(
        chat_id=chat_id,
        column=User.verified,
    )

    return verified if verified else False
