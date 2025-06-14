from aiogram import Dispatcher

from tg2go.bot.handlers.client.commands import start


def RegisterClientHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        start.router,
    )
