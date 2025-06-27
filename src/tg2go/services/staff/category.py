from __future__ import annotations

from tg2go.db.models.common.types import CategoryId
from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.repositories.good import GoodRepository
from tg2go.db.session import AsyncSessionLocal


class StaffCategoryService:
    def __init__(self, cat_repo: CategoryRepository, good_repo: GoodRepository):
        self._cat = cat_repo
        self._good = good_repo

        # --- Create ---
        self.InsertNewCategory = self._cat.InsertNewCategory

        # --- Read ---
        self.GetCategory = self._cat.GetCategory
        self.GetSortedCategories = self._cat.GetSortedCategories

        # --- Update ---
        self.UpdateCategory = self._cat.UpdateCategory

    @staticmethod
    def Create() -> StaffCategoryService:
        return StaffCategoryService(
            cat_repo=CategoryRepository(AsyncSessionLocal),
            good_repo=GoodRepository(AsyncSessionLocal),
        )

    # --- Delete ---
    async def InvalidateCategory(self, category_id: CategoryId) -> None:
        goods = await self._good.GetAvailableGoods(category_id)

        for good in goods:
            await self._good.InvalidateGood(good.good_id)

        await self._cat.InvalidateCategory(category_id)
