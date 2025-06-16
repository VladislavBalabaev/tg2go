from tg2go.db.models.user import User
from tg2go.db.services.user_context import GetContextService


async def CheckConfirmedd(chat_id: int) -> bool:
    ctx = GetContextService()

    confirmed = await ctx.GetUser(
        chat_id=chat_id,
        column=User.confirmed,
    )

    return confirmed if confirmed else False
