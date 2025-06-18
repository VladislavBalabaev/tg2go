from __future__ import annotations

from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.session import AsyncSessionLocal


class StaffCategoryService:
    def __init__(self, cat_repo: CategoryRepository):
        self.cat_repo = cat_repo

        # --- Create ---
        self.InsertNewCategory = self.cat_repo.InsertNewCategory

        # --- Read ---
        self.GetCategories = self.cat_repo.GetCategories

        # --- Update ---
        self.UpdateCategoryName = self.cat_repo.UpdateCategoryName

        # --- Delete ---
        self.InvalidateCategory = self.cat_repo.InvalidateCategory

    @staticmethod
    def Create() -> StaffCategoryService:
        return StaffCategoryService(CategoryRepository(AsyncSessionLocal))
