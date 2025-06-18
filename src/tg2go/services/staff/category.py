from __future__ import annotations

from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.session import AsyncSessionLocal


class StaffCategoryService:
    def __init__(self, cat_repo: CategoryRepository):
        self._cat = cat_repo

        # --- Create ---
        self.InsertNewCategory = self._cat.InsertNewCategory

        # --- Read ---
        self.GetCategories = self._cat.GetCategories

        # --- Update ---
        self.UpdateCategoryName = self._cat.UpdateCategoryName

        # --- Delete ---
        self.InvalidateCategory = self._cat.InvalidateCategory

    @staticmethod
    def Create() -> StaffCategoryService:
        return StaffCategoryService(CategoryRepository(AsyncSessionLocal))
