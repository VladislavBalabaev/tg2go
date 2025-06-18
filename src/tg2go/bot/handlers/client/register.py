from aiogram import Dispatcher

from tg2go.bot.handlers.client.commands import start_hub, start_register


def RegisterClientHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        # order matters
        start_hub.router,
        start_register.router,
    )
