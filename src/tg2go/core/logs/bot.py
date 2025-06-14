import logging
from logging.handlers import QueueListener

from tg2go.core.configs.paths import PATH_BOT_LOGS
from tg2go.core.logs.settings import (
    CreateConsoleHandler,
    CreateFileHandler,
    CreateListener,
    FilterOutLogs,
)


async def LoggerSetup() -> QueueListener:
    console_handler = CreateConsoleHandler(
        logging.INFO,
        filters=[
            FilterOutLogs("sqlalchemy.engine", logging.WARNING),
            FilterOutLogs("aiogram", logging.WARNING),
        ],
    )
    bot_file_handler = CreateFileHandler(
        PATH_BOT_LOGS,
        logging.DEBUG,
    )

    listener: QueueListener = CreateListener(console_handler, bot_file_handler)

    return listener
