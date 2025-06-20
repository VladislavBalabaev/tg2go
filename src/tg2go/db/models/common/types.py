from enum import Enum
from typing import NewType


# TODO: add more order statuses
class OrderStatus(str, Enum):
    created = "created"
    pending = "pending"
    paid = "paid"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


CategoryId = NewType("CategoryId", int)
OrderId = NewType("OrderId", int)
GoodId = NewType("GoodId", int)
OrderItemId = NewType("OrderItemId", int)
