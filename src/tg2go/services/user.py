from tg2go.db.models.user import User
from tg2go.db.repositories.user import UserRepository
from tg2go.db.session import AsyncSessionLocal


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

        # --- Create ---
        self.CreateUser = self.user_repo.CreateUser

        # --- Read ---
        self.GetUsersOnCondition = self.user_repo.GetUsersOnCondition
        self.GetUser = self.user_repo.GetUser

        # --- Update ---
        self.UpdateUser = self.user_repo.UpdateUser

    # --- Read ---
    async def CheckUserExists(self, chat_id: int) -> bool:
        result = await self.GetUser(
            chat_id=chat_id,
            column=User.chat_id,
        )

        return result is not None

    async def GetVerifiedUsersChatId(self) -> list[int]:
        result = await self.GetUsersOnCondition(
            condition=User.verified,
            column=User.chat_id,
        )

        return result

    async def GetChatIdByUsername(self, username: str) -> int | None:
        result = await self.GetUsersOnCondition(
            condition=User.username == username,
            column=User.chat_id,
        )

        return int(result[0]) if result else None


def GetUserService() -> UserService:
    return UserService(UserRepository(AsyncSessionLocal))
