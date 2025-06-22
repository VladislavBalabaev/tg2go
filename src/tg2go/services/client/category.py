from __future__ import annotations

from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.session import AsyncSessionLocal


class ClientCategoryService:
    def __init__(self, cat_repo: CategoryRepository):
        self._cat = cat_repo

        # --- Read ---
        self.GetCategory = self._cat.GetCategory
        self.GetSortedCategories = self._cat.GetSortedCategories

    @staticmethod
    def Create() -> ClientCategoryService:
        return ClientCategoryService(CategoryRepository(AsyncSessionLocal))
