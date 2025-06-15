from tg2go.db.models.user import User
from tg2go.db.repositories.user import UserRepository


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

    async def GetConfirmedUsersChatId(self) -> list[int]:
        result = await self.GetUsersOnCondition(
            condition=User.confirmed,
            column=User.chat_id,
        )

        return result
