from __future__ import annotations

from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.repositories.good import GoodRepository
from tg2go.db.session import AsyncSessionLocal


class ClientGoodService:
    def __init__(self, cat_repo: CategoryRepository, good_repo: GoodRepository):
        self._cat = cat_repo
        self._good = good_repo

        # --- Read ---
        self.GetSortedCategories = self._cat.GetSortedCategories
        self.GetAvailableGoods = self._good.GetAvailableGoods

    @staticmethod
    def Create() -> ClientGoodService:
        return ClientGoodService(
            cat_repo=CategoryRepository(AsyncSessionLocal),
            good_repo=GoodRepository(AsyncSessionLocal),
        )
