import logging
from typing import Any

from sqlalchemy import event, insert
from sqlalchemy.engine import Connection

from tg2go.db.models.order import Order
from tg2go.db.models.order_history import OrderHistory


@event.listens_for(Order, "after_insert", propagate=True)
def _SaveToOrderHistoryOnInsert(
    mapper: Any,
    connection: Connection,
    target: Order,
) -> None:
    stmt = insert(OrderHistory).values(
        order_id=target.order_id,
        chat_id=target.chat_id,
        status=target.status,
        total_price_rub=target.total_price_rub,
        internal_comment=target.internal_comment,
        client_comment=target.client_comment,
        updated_at=target.created_at,
    )
    connection.execute(stmt)

    logging.info(
        f"OrderItem(order_id={target.order_id}, updated_at={target.created_at}) is inserted upon order insertion."
    )


@event.listens_for(Order, "after_update", propagate=True)
def _SaveToOrderHistoryOnUpdate(
    mapper: Any,
    connection: Connection,
    target: Order,
) -> None:
    stmt = insert(OrderHistory).values(
        order_id=target.order_id,
        chat_id=target.chat_id,
        status=target.status,
        total_price_rub=target.total_price_rub,
        internal_comment=target.internal_comment,
        client_comment=target.client_comment,
        updated_at=target.updated_at,
    )

    connection.execute(stmt)

    logging.info(
        f"OrderItem(order_id={target.order_id}, updated_at={target.created_at}) is updated upon order update."
    )
