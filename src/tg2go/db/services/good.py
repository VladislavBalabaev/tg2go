from tg2go.db.repositories.good import GoodRepository


class GoodService:
    def __init__(self, good_repo: GoodRepository):
        self.good_repo = good_repo

        # --- Create ---
        self.AddGood = self.good_repo.AddGood

        # --- Read ---
        self.GetAvailableGoods = self.good_repo.GetAvailableGoods

        # --- Update ---
        self.UpdateGood = self.good_repo.UpdateGood

        # --- Delete ---
        self.InvalidateGood = self.good_repo.InvalidateGood
