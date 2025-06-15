from tg2go.db.repositories.order import OrderRepository


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

        # --- Create ---
        self.CreateNewOrder = self.order_repo.CreateNewOrder

        # --- Update ---
        self.AddGoodToOrder = self.order_repo.AddGoodToOrder
        self.RemoveGoodFromOrder = self.order_repo.RemoveGoodFromOrder
