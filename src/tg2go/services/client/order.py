from __future__ import annotations

from decimal import Decimal

from tg2go.bot.lib.message.io import DeleteMessage
from tg2go.db.models.order import Order, OrderId
from tg2go.db.models.user import User
from tg2go.db.repositories.good import GoodRepository
from tg2go.db.repositories.order import OrderRepository
from tg2go.db.repositories.user import UserRepository
from tg2go.db.session import AsyncSessionLocal


async def CreateNewOrder(chat_id: int) -> OrderId:
    order_repo = OrderRepository(AsyncSessionLocal)
    user_repo = UserRepository(AsyncSessionLocal)

    order_id = await order_repo.CreateNewOrder(chat_id)

    await user_repo.UpdateUser(
        chat_id=chat_id,
        column=User.current_order_id,
        value=order_id,
    )

    return order_id


class ClientOrderService:
    def __init__(
        self,
        chat_id: int,
        order_id: OrderId,
        good_repo: GoodRepository,
        order_repo: OrderRepository,
        user_repo: UserRepository,
    ):
        self.chat_id = chat_id
        self.order_id = order_id
        self.good = good_repo
        self.order = order_repo
        self.user = user_repo

    async def _GetOrder(self) -> Order:
        order = await self.order.GetOrder(self.order_id)

        if order is None:
            raise ValueError(f"Order(order_id={self.order_id}) doesn't exist.")

        return order

    async def DeleteOrderMessage(self) -> None:
        order = await self._GetOrder()

        if order.order_message_id is None:
            raise ValueError(
                f"Order(order_id={self.order_id}) doesn't have order_message_id already."
            )

        await DeleteMessage(chat_id=self.chat_id, message_id=order.order_message_id)

    async def DeleteGoodMessage(self) -> None:
        order = await self._GetOrder()

        if order.good_message_id is not None:
            await DeleteMessage(chat_id=self.chat_id, message_id=order.good_message_id)

    async def OrderInfo(self) -> str:
        order = await self._GetOrder()

        info = "Шаурма #1 / Сокольники\n📍Москва, Сокольническая площадь, 9\n\n"

        if order.order_items:
            info += "Выберите категорию меню."
            return info

        info += "Заказ:\n"

        for i, item in enumerate(order.order_items, 1):
            name: str = item.good.name
            qty: int = item.quantity
            price: Decimal = item.unit_price_rub

            info += f"{i}. {name} - {qty} шт. × {price}₽ = {price * qty}₽\n"

        info += f"\nИтого: {order.total_price_rub}₽"

        return info

    async def OrderInfoCategories(self) -> list[str]:
        return ["вкусновое", "невкусновое", "пирожки", "кошкимышки"]

    async def FinishOrdering(self) -> None:
        # TODO: FinishOrderOrdering
        ...

    @staticmethod
    async def Create(chat_id: int) -> ClientOrderService:
        good_repo = GoodRepository(AsyncSessionLocal)
        order_repo = OrderRepository(AsyncSessionLocal)
        user_repo = UserRepository(AsyncSessionLocal)

        order_id = await user_repo.GetUser(
            chat_id=chat_id, column=User.current_order_id
        )

        if order_id is None:
            raise ValueError(f"User(chat_id={chat_id}) doesn't have current order.")

        return ClientOrderService(
            chat_id=chat_id,
            order_id=order_id,
            good_repo=good_repo,
            order_repo=order_repo,
            user_repo=user_repo,
        )
