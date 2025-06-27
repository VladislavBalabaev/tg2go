from aiogram import Dispatcher

from tg2go.bot.handlers.forall.commands import cancel, zero


def RegisterHandlerCancel(dp: Dispatcher) -> None:
    dp.include_routers(
        cancel.router,
    )


def RegisterHandlerZeroMessage(dp: Dispatcher) -> None:
    dp.include_routers(
        zero.router,
    )
