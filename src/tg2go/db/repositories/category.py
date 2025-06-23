import logging
from typing import TypeVar

from sqlalchemy import desc, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute

from tg2go.db.models.category import Category
from tg2go.db.models.common.types import CategoryId

T = TypeVar("T")


class CategoryRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # --- Create ---
    async def InsertNewCategory(self, name: str, index: int) -> None:
        category = Category(name=name, index=index)

        async with self.session() as session:
            try:
                session.add(category)
                await session.commit()
                logging.info(f"{category} inserted successfully.")
            except IntegrityError:
                await session.rollback()
                logging.error(f"{category} already exists. Insertion failed.")
                raise

    # --- Read ---
    async def GetCategory(self, category_id: CategoryId) -> Category:
        async with self.session() as session:
            result = await session.execute(
                select(Category).where(Category.category_id == category_id)
            )

            categories = list(result.scalars().all())
            if len(categories) != 1:
                raise NoResultFound(f"No Category(category_id={category_id}) found.")

            return categories[0]

    async def GetSortedCategories(self) -> list[Category]:
        async with self.session() as session:
            result = await session.execute(
                select(Category)
                .where(Category.valid.is_(True))
                .order_by(desc(Category.index))
            )

            categories = list(result.scalars().all())
            categories.sort(key=lambda x: x.index)

            return categories

    # --- Update ---
    async def UpdateCategory(
        self,
        category_id: CategoryId,
        column: InstrumentedAttribute[T],
        value: T,
    ) -> None:
        async with self.session() as session:
            result = await session.execute(
                update(Category)
                .where(Category.category_id == category_id)
                .values({column.key: value})
            )

            if result.rowcount == 0:
                raise NoResultFound(
                    f"Failed to update: '{column}={value}'. No Category(category_id={category_id}) found."
                )

            await session.commit()

        logging.info(
            f"Category(category_id={category_id}) updated: '{column}={value}' successfully."
        )

    # --- Delete ---
    async def InvalidateCategory(self, category_id: CategoryId) -> None:
        async with self.session() as session:
            result = await session.execute(
                update(Category)
                .where(Category.category_id == category_id)
                .values({Category.valid: False})
            )

            if result.rowcount == 0:
                raise NoResultFound(
                    f"Failed to invalidate category. No Category(category_id={category_id}) found."
                )

            await session.commit()

        logging.info(f"Category(category_id={category_id}) is invalidated.")
