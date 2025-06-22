from __future__ import annotations

from tg2go.db.repositories.good import GoodRepository
from tg2go.db.session import AsyncSessionLocal


class ClientGoodService:
    def __init__(self, good_repo: GoodRepository):
        self._good = good_repo

        # --- Read ---
        self.GetGood = self._good.GetGood
        self.GetAvailableGoods = self._good.GetAvailableGoods

    @staticmethod
    def Create() -> ClientGoodService:
        return ClientGoodService(
            good_repo=GoodRepository(AsyncSessionLocal),
        )
