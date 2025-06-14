from typing import Any

from sqlalchemy.orm.attributes import InstrumentedAttribute

from tg2go.db.base import Base


def CheckColumnBelongsToModel(
    column: InstrumentedAttribute[Any], model: type[Base]
) -> None:
    if column.property.parent.class_ is not model:
        raise ValueError(
            f"Provided column does not belong to the {model.__name__} model."
        )


def CheckOnlyOneArgProvided(**kwargs: Any) -> None:
    provided = [key for key, value in kwargs.items() if value is not None]

    if len(provided) != 1:
        raise ValueError(f"More than one argument is provided: {', '.join(provided)}.")
