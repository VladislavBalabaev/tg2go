import logging
from typing import TypeVar

from sqlalchemy import desc, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute

from tg2go.db.models.good import Good, GoodId

T = TypeVar("T")


class GoodRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # ----- Create -----
    async def InsertNewGood(self, good: Good) -> None:
        async with self.session() as session:
            try:
                session.add(good)
                await session.commit()
                logging.info(f"{good} inserted successfully.")
            except IntegrityError:
                await session.rollback()
                logging.error(f"{good} already exists. Insertion failed.")
                raise

    async def GetAvailableGoods(self) -> list[Good]:
        async with self.session() as session:
            result = await session.execute(
                select(Good).where(Good.available).order_by(desc(Good.category))
            )

            return list(result.scalars().all())

    # ----- Update -----
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

    # ----- Delete -----
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
