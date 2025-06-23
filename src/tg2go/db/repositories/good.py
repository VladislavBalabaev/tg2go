import logging
from decimal import Decimal
from typing import TypeVar

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute

from tg2go.db.models.category import Category
from tg2go.db.models.common.types import CategoryId, GoodId
from tg2go.db.models.good import Good

T = TypeVar("T")


class GoodRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # --- Create ---
    async def InsertNewGood(
        self,
        category_id: CategoryId,
        name: str,
        price_rub: Decimal,
        description: str,
        image_file_id: str,
    ) -> None:
        good = Good(
            name=name,
            price_rub=price_rub,
            description=description,
            image_file_id=image_file_id,
            category_id=category_id,
        )

        async with self.session() as session:
            try:
                session.add(good)
                await session.commit()
                logging.info(f"{good} inserted successfully.")
            except IntegrityError:
                await session.rollback()
                logging.error(f"{good} already exists. Insertion failed.")
                raise

    # --- Read ---
    async def GetGood(self, good_id: GoodId) -> Good:
        async with self.session() as session:
            result = await session.execute(select(Good).where(Good.good_id == good_id))

            goods = list(result.scalars().all())
            if len(goods) != 1:
                raise NoResultFound(f"No Good(good_id={good_id}) found.")

            return goods[0]

    async def GetAvailableGoods(self, category_id: CategoryId) -> list[Good]:
        async with self.session() as session:
            result = await session.execute(
                select(Good)
                .options(selectinload(Good.category))
                .join(Good.category)
                .where(
                    Good.available.is_(True),
                    Category.category_id == category_id,
                )
            )

            return list(result.scalars().all())

    # --- Update ---
    async def UpdateGood(
        self,
        good_id: GoodId,
        column: InstrumentedAttribute[T],
        value: T,
    ) -> None:
        async with self.session() as session:
            result = await session.execute(
                update(Good).where(Good.good_id == good_id).values({column.key: value})
            )

            if result.rowcount == 0:
                raise NoResultFound(
                    f"Failed to update: '{column}={value}'. No Good(good_id={good_id}) found."
                )

            await session.commit()

        logging.info(
            f"Good(good_id={good_id}) updated: '{column}={value}' successfully."
        )

    # --- Delete ---
    async def InvalidateGood(self, good_id: GoodId) -> None:
        async with self.session() as session:
            result = await session.execute(
                update(Good)
                .where(Good.good_id == good_id)
                .values(
                    {
                        Good.available: False,
                        Good.valid: False,
                    }
                )
            )

            if result.rowcount == 0:
                raise NoResultFound(
                    f"Failed to invalidate good. No Good(good_id={good_id}) found."
                )

            await session.commit()

        logging.info(f"Good(good_id={good_id}) is invalidated.")
