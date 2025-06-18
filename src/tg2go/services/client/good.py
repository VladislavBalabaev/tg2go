from tg2go.db.repositories.category import CategoryRepository
from tg2go.db.repositories.good import GoodRepository
from tg2go.db.session import AsyncSessionLocal


class GoodService:
    def __init__(self, cat_repo: CategoryRepository, good_repo: GoodRepository):
        self.cat_repo = cat_repo
        self.good_repo = good_repo

        # --- Create ---
        self.InsertNewCategory = self.cat_repo.InsertNewCategory
        self.InsertNewGood = self.good_repo.InsertNewGood

        # --- Read ---
        self.GetCategories = self.cat_repo.GetCategories
        self.GetAvailableGoods = self.good_repo.GetAvailableGoods

        # --- Update ---
        self.UpdateCategoryName = self.cat_repo.UpdateCategoryName
        self.UpdateGood = self.good_repo.UpdateGood

        # --- Delete ---
        self.InvalidateCategory = self.cat_repo.InvalidateCategory
        self.InvalidateGood = self.good_repo.InvalidateGood


def GetGoodService() -> GoodService:
    return GoodService(
        cat_repo=CategoryRepository(AsyncSessionLocal),
        good_repo=GoodRepository(AsyncSessionLocal),
    )
