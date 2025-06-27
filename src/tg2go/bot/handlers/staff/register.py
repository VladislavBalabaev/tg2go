from aiogram import Dispatcher

from tg2go.bot.handlers.staff.callbacks import panel, settings
from tg2go.bot.handlers.staff.callbacks.category import (
    add as cat_add,
    category,
    change as cat_change,
    remove as cat_remove,
)
from tg2go.bot.handlers.staff.callbacks.good import (
    add as good_add,
    change as good_change,
    good,
    remove as good_remove,
)
from tg2go.bot.handlers.staff.commands import staff


def RegisterStaffHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        staff.router,
        panel.router,
        settings.router,
        category.router,
        cat_add.router,
        cat_change.router,
        cat_remove.router,
        good.router,
        good_add.router,
        good_change.router,
        good_remove.router,
    )
