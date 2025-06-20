import asyncio

from tg2go.bot.handlers.admin.register import RegisterAdminHandlers
from tg2go.bot.handlers.client.register import RegisterClientHandlers
from tg2go.bot.handlers.common.register import (
    RegisterHandlerCancel,
    RegisterHandlerZeroMessage,
)
from tg2go.bot.handlers.staff.register import RegisterStaffHandlers
from tg2go.bot.lib.message.middleware import SetBotMiddleware
from tg2go.bot.lib.notifications import admin
from tg2go.bot.lib.notifications.erroring import SetExceptionHandlers
from tg2go.bot.lib.notifications.pending import ProcessPendingUpdates
from tg2go.bot.lifecycle.creator import bot, dp
from tg2go.bot.lifecycle.menu import SetMenu
from tg2go.core.configs.paths import EnsurePaths
from tg2go.core.logs import flow as logs
from tg2go.core.logs.bot import LoggerSetup
from tg2go.db.session import EnsureDB


async def EnsureDependencies() -> None:
    await EnsureDB()


async def OnStartup() -> None:
    await SetMenu()
    RegisterHandlerCancel(dp)
    RegisterAdminHandlers(dp)
    RegisterStaffHandlers(dp)
    RegisterClientHandlers(dp)
    RegisterHandlerZeroMessage(dp)
    SetBotMiddleware(dp)

    await admin.NotifyOnStartup()
    await ProcessPendingUpdates()


async def OnShutdown() -> None:
    await admin.NotifyOnShutdown()

    await logs.LoggerShutdown()


async def main() -> None:
    EnsurePaths()
    await logs.LoggerStart(LoggerSetup)

    await EnsureDependencies()

    dp.startup.register(OnStartup)
    dp.shutdown.register(OnShutdown)

    SetExceptionHandlers()

    await dp.start_polling(bot, drop_pending_updates=True)


# $ python -m nespresso
if __name__ == "__main__":
    asyncio.run(main())
