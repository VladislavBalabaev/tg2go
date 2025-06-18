import logging

from tg2go.bot.lib.chat.username import GetChatUserLoggingPart
from tg2go.db.models.order import Order, OrderStatus
from tg2go.db.models.user import User
from tg2go.db.repositories.good import GoodRepository
from tg2go.db.repositories.order import OrderRepository
from tg2go.db.repositories.user import UserRepository
from tg2go.db.session import AsyncSessionLocal


class OrderService:
    def __init__(
        self,
        good_repo: GoodRepository,
        order_repo: OrderRepository,
        user_repo: UserRepository,
    ):
        self.good = good_repo
        self.order = order_repo
        self.user = user_repo

    async def CancelCurrentOrder(self, chat_id: int) -> Order | None:
        order_id = await self.user.GetUser(chat_id=chat_id, column=User.order_id)

        if order_id is None:
            return None

        await self.user.UpdateUser(
            chat_id=chat_id,
            column=User.order_id,
            value=None,
        )

        await self.order.UpdateOrder(
            order_id=order_id,
            column=Order.status,
            value=OrderStatus.cancelled,
        )

        order = await self.order.GetOrder(order_id=order_id)

        part = await GetChatUserLoggingPart(chat_id)
        logging.info(f"{part} :: {order} is cancelled.")

        return order

    async def CreateNewOrder(self, chat_id: int) -> None:
        order_id = await self.order.CreateNewOrder(chat_id)

        await self.user.UpdateUser(
            chat_id=chat_id,
            column=User.order_id,
            value=order_id,
        )

        # await SendMessage(
        #     chat_id=chat_id,
        #     text=...,
        #     reply_markup=...,
        # )

    async def _GenerateOrderSummary(self, chat_id: int) -> str:
        return ""

    async def UpdateOrderMessage(self, chat_id: int) -> None:
        summary = await self._GenerateOrderSummary(chat_id)
        # await SendMessage(
        #     chat_id=chat_id,
        #     text=summary,
        # )

    # ----- Read -----
    # async def GetOrderStatus(self, order_id: OrderId) -> OrderStatus:
    #     order = await self.GetOrder(order_id)

    #     if order is None:
    #         raise ValueError(f"Trying to access status of Order(order_id={order_id}) which doesn't exist.")

    #     return order.status


def GetOrderService() -> OrderService:
    return OrderService(
        good_repo=GoodRepository(AsyncSessionLocal),
        order_repo=OrderRepository(AsyncSessionLocal),
        user_repo=UserRepository(AsyncSessionLocal),
    )
