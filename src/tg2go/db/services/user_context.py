from tg2go.db.repositories.message import MessageRepository
from tg2go.db.repositories.nes_user import NesUserRepository
from tg2go.db.repositories.tg_user import TgUserRepository
from tg2go.db.services.message import MessageService
from tg2go.db.services.user import UserService
from tg2go.db.session import AsyncSessionLocal


class UserContextService(UserService, MessageService):
    """
    Combines UserService and MessageService into a single context service.
    Inherits methods from both services.
    """

    def __init__(self, user_service: UserService, message_service: MessageService):
        # Initialize both parent classes explicitly
        UserService.__init__(
            self,
            tg_user_repo=user_service.tg_user_repo,
            nes_user_repo=user_service.nes_user_repo,
        )
        MessageService.__init__(self, message_service.message_repo)

    # async def ...


async def GetUserContextService() -> UserContextService:
    tg_user_repo = TgUserRepository(AsyncSessionLocal)
    nes_user_repo = NesUserRepository(AsyncSessionLocal)
    message_repo = MessageRepository(AsyncSessionLocal)

    user_service = UserService(tg_user_repo=tg_user_repo, nes_user_repo=nes_user_repo)
    message_service = MessageService(message_repo)

    return UserContextService(user_service, message_service)
