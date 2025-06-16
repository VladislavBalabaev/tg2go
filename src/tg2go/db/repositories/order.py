import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tg2go.db.models.good import Good, GoodId
from tg2go.db.models.order import CreateOrder, Order, OrderId
from tg2go.db.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # ----- Create -----
    async def CreateNewOrder(self, chat_id: int) -> OrderId:
        order = CreateOrder(chat_id=chat_id)

        async with self.session() as session:
            session.add(order)
            await session.commit()

        logging.info(f"{order} created successfully.")

        return order.order_id

    # ----- Update -----
    async def AddGoodToOrder(self, order_id: OrderId, good_id: GoodId) -> None:
        async with self.session() as session:
            order = await session.get(Order, order_id)
            good = await session.get(Good, good_id)

            if order is None:
                raise ValueError(
                    f"No such Order(order_id={order_id}) when adding good to order."
                )
            if good is None:
                raise ValueError(
                    f"No such Good(good_id={good_id}) when adding good to order."
                )

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
                order.order_items.append(item)

            order.total_price_rub += item.unit_price_rub

            logging.info(f"After adding good {good} order is {order}")

            await session.commit()

    async def RemoveGoodFromOrder(self, order_id: OrderId, good_id: GoodId) -> None:
        async with self.session() as session:
            order = await session.get(Order, order_id)
            good = await session.get(Good, good_id)

            if order is None:
                raise ValueError(
                    f"No such Order(order_id={order_id}) when removing good from order."
                )
            if good is None:
                raise ValueError(
                    f"No such Good(good_id={good_id}) when removing good from order."
                )

            for item in order.order_items:
                if good.good_id == item.good_id:
                    item.quantity -= 1
                    break
            else:
                raise ValueError(f"No {good} in {order} when removing good from order.")

            order.total_price_rub -= item.unit_price_rub

            if item.quantity == 0:
                await session.delete(item)

            if order.total_price_rub < 0:
                await session.rollback()
                raise ValueError(f"Total price RUB is negative for {order}")

            logging.info(f"After removing good {good} order is {order}")

            await session.commit()
