from tg2go.db.repositories.good import GoodRepository
from tg2go.db.repositories.order import OrderRepository
from tg2go.db.repositories.user import UserRepository
from tg2go.db.services.good import GoodService
from tg2go.db.services.order import OrderService
from tg2go.db.services.user import UserService
from tg2go.db.session import AsyncSessionLocal


class ContextService(UserService, GoodService, OrderService):
    def __init__(
        self,
        good_repo: GoodRepository,
        order_repo: OrderRepository,
        user_repo: UserRepository,
    ):
        GoodService.__init__(self, good_repo)
        OrderService.__init__(self, order_repo)
        UserService.__init__(self, user_repo)

    # async def ...


def GetContextService() -> ContextService:
    context_service = ContextService(
        good_repo=GoodRepository(AsyncSessionLocal),
        order_repo=OrderRepository(AsyncSessionLocal),
        user_repo=UserRepository(AsyncSessionLocal),
    )

    return context_service
