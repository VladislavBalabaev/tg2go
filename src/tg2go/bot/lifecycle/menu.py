from aiogram.types import BotCommand

from tg2go.bot.lifecycle.creator import bot


async def SetMenu() -> None:
    commands = [
        BotCommand(command="/start", description="Регистрация"),
        BotCommand(command="/find", description="Поиск выпускников"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/help", description="Помощь"),
    ]

    await bot.set_my_commands(commands)
