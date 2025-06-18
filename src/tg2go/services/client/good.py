from __future__ import annotations

from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.repositories.good import GoodRepository
from tg2go.db.session import AsyncSessionLocal


class ClientGoodService:
    def __init__(self, cat_repo: CategoryRepository, good_repo: GoodRepository):
        self.cat_repo = cat_repo
        self.good_repo = good_repo

        # --- Read ---
        self.GetCategories = self.cat_repo.GetCategories
        self.GetAvailableGoods = self.good_repo.GetAvailableGoods

    @staticmethod
    def Create() -> ClientGoodService:
        return ClientGoodService(
            cat_repo=CategoryRepository(AsyncSessionLocal),
            good_repo=GoodRepository(AsyncSessionLocal),
        )
