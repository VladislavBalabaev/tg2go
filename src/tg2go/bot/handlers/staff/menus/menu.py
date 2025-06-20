from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup


@dataclass
class Menu:
    text: str
    reply_markup: InlineKeyboardMarkup | None
