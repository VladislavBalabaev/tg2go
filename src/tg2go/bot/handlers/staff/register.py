from aiogram import Dispatcher

from tg2go.bot.handlers.staff.callbacks import category, good, settings, staff as stff
from tg2go.bot.handlers.staff.callbacks.category_action import add as category_add
from tg2go.bot.handlers.staff.callbacks.good_action import add as good_add
from tg2go.bot.handlers.staff.commands import staff


def RegisterStaffHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        staff.router,
        stff.router,
        settings.router,

        category.router,
        category_add.router,

        good.router,
        good_add.router,
    )
