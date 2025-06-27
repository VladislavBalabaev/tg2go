import logging
from decimal import Decimal
from typing import TypeVar, overload

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

from tg2go.db.models.common.types import GoodId, OrderId, OrderItemId
from tg2go.db.models.good import Good
from tg2go.db.models.order import Order
from tg2go.db.models.order_item import OrderItem

T = TypeVar("T")


class OrderRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # --- Create ---
    async def CreateNewOrder(self, chat_id: int) -> OrderId:
        order = Order(chat_id=chat_id)

        async with self.session() as session:
            session.add(order)
            await session.commit()

        logging.info(f"{order} created successfully.")

        return order.order_id

    # --- Read ---
    @overload
    async def GetOrdersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: None = None,
    ) -> list[Order]: ...

    @overload
    async def GetOrdersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: InstrumentedAttribute[T],
    ) -> list[T]: ...

    async def GetOrdersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: InstrumentedAttribute[T] | None = None,
    ) -> list[Order] | list[T]:
        selection = Order
        if column is not None:
            selection = getattr(Order, column.key)

        async with self.session() as session:
            result = await session.execute(
                select(selection)
                .options(selectinload(Order.order_items))
                .where(condition)
            )

        return list(result.scalars().all())

    @overload
    async def GetOrder(
        self,
        order_id: OrderId,
        column: None = None,
    ) -> Order | None: ...

    @overload
    async def GetOrder(
        self,
        order_id: OrderId,
        column: InstrumentedAttribute[T],
    ) -> T | None: ...

    async def GetOrder(
        self,
        order_id: OrderId,
        column: InstrumentedAttribute[T] | None = None,
    ) -> Order | T | None:
        result = await self.GetOrdersOnCondition(
            condition=Order.order_id == order_id,
            column=column,
        )

        return result[0] if result else None

    # --- Update ---
    async def UpdateOrder(
        self,
        order_id: OrderId,
        column: InstrumentedAttribute[T],
        value: T,
    ) -> None:
        async with self.session() as session:
            result = await session.execute(
                update(Order)
                .where(Order.order_id == order_id)
                .values({column.key: value})
            )

            if result.rowcount == 0:
                logging.error(
                    f"Failed to update: '{column}={value}'. No Order(order_id={order_id}) found."
                )
                raise NoResultFound()

            await session.commit()
            logging.info(
                f"Order(order_id={order_id}) updated: '{column}={value}' successfully."
            )

    # --- Order-Good Logic ---
    async def AddGoodInOrder(
        self,
        order_id: OrderId,
        good_id: GoodId,
    ) -> OrderItemId:
        async with self.session() as session:
            order = await session.get(Order, order_id)
            good = await session.get(Good, good_id)

            if order is None:
                raise ValueError(f"No such Order(order_id={order_id}).")
            if good is None:
                raise ValueError(f"No such Good(good_id={good_id}).")

            for item in order.order_items:
                if good.good_id == item.good_id:
                    item.quantity += 1
                    break
            else:
                item = OrderItem(
                    order=order,
                    good=good,
                    quantity=1,
                    unit_price_rub=good.price_rub,  # cache
                )
                order.order_items.append(item)  # do i need to do it?

            order.total_price_rub += item.unit_price_rub

            logging.info(f"After adding {good} order is {order}")

            await session.commit()

        return item.order_item_id

    async def ReduceGoodInOrder(
        self,
        order_id: OrderId,
        good_id: GoodId,
    ) -> OrderItemId:
        async with self.session() as session:
            order = await session.get(Order, order_id)
            good = await session.get(Good, good_id)

            if order is None:
                raise ValueError(f"No such Order(order_id={order_id}).")
            if good is None:
                raise ValueError(f"No such Good(good_id={good_id}).")

            for item in order.order_items:
                if good.good_id == item.good_id:
                    item.quantity -= 1
                    break
            else:
                raise ValueError(
                    f"No such OrderItem(good_id={good_id}) was found in Order(order_id={order_id})."
                )

            order.total_price_rub -= item.unit_price_rub

            if item.quantity == 0:
                await session.delete(item)

            if order.total_price_rub < 0:
                await session.rollback()
                raise ValueError(f"Total price RUB is negative for {order}")

            logging.info(f"After removing {good} order is {order}")

            await session.commit()

        return item.order_item_id

    async def RemoveAllItemsFromOrder(self, order_id: OrderId) -> OrderItemId:
        async with self.session() as session:
            order = await session.get(Order, order_id)

            if order is None:
                raise ValueError(f"No such Order(order_id={order_id}).")

            for item in order.order_items:
                logging.info(f"Remove {item} from {order}")
                await session.delete(item)

            order.total_price_rub = Decimal("0.0")

            await session.commit()

        return item.order_item_id
