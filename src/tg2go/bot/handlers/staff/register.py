from aiogram import Dispatcher

from tg2go.bot.handlers.staff.commands import staff


def RegisterAdminHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        staff.router,
    )
