from enum import Enum
from typing import NewType
from uuid import UUID


# TODO: add more order statuses
class OrderStatus(str, Enum):
    created = "created"
    pending = "pending"
    paid = "paid"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


CategoryId = NewType("CategoryId", UUID)
GoodId = NewType("GoodId", UUID)
OrderItemId = NewType("OrderItemId", int)
OrderId = NewType("OrderId", UUID)
