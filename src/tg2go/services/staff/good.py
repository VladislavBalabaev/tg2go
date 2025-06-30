from __future__ import annotations

from tg2go.db.repositories.good import GoodRepository
from tg2go.db.session import AsyncSessionLocal


class StaffGoodService:
    def __init__(self, good_repo: GoodRepository):
        self._good = good_repo

        # --- Create ---
        self.InsertNewGood = self._good.InsertNewGood

        # --- Read ---
        self.GetGood = self._good.GetGood
        self.GetValidGoods = self._good.GetValidGoods

        # --- Update ---
        self.UpdateGood = self._good.UpdateGood

        # --- Delete ---
        self.InvalidateGood = self._good.InvalidateGood

    @staticmethod
    def Create() -> StaffGoodService:
        return StaffGoodService(
            good_repo=GoodRepository(AsyncSessionLocal),
        )
