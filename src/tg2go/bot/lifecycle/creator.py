from aiogram import Bot, Dispatcher

from tg2go.core.configs.settings import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value())

dp = Dispatcher()


BOT_ID = bot.id
