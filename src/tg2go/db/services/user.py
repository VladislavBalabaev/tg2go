from tg2go.db.models.clients import TgUser
from tg2go.db.repositories.nes_user import NesUserRepository
from tg2go.db.repositories.tg_user import TgUserRepository


class UserService:
    def __init__(
        self, tg_user_repo: TgUserRepository, nes_user_repo: NesUserRepository
    ):
        self.tg_user_repo = tg_user_repo
        self.nes_user_repo = nes_user_repo

        # --- Create ---
        # - Tg -
        self.RegisterTgUser = self.tg_user_repo.CreateTgUser

        # - Nes -
        self.UpsertNesUser = self.nes_user_repo.UpsertNesUsers

        # --- Read ---
        # - Tg -
        self.GetTgUsersOnCondition = self.tg_user_repo.GetTgUsersOnCondition
        self.GetTgUser = self.tg_user_repo.GetTgUser
        self.GetTgChatIdBy = self.tg_user_repo.GetChatIdBy

        # - Nes -
        self.GetNesUsersOnCondition = self.nes_user_repo.GetNesUsersOnCondition
        self.GetNesUser = self.nes_user_repo.GetNesUser

        # --- Update ---
        # - Tg -
        self.UpdateTgUser = self.tg_user_repo.UpdateTgUser

        # --- Delete ---

    # --- Create ---

    # --- Read ---
    # - Tg -
    async def CheckTgUserExists(self, chat_id: int) -> bool:
        result = await self.GetTgUser(
            chat_id=chat_id,
            column=TgUser.chat_id,
        )

        return result is not None

    async def GetVerifiedTgUsersChatId(self) -> list[int]:
        result = await self.GetTgUsersOnCondition(
            condition=TgUser.verified,
            column=TgUser.chat_id,
        )

        return result

    # --- Update ---

    # --- Delete ---
