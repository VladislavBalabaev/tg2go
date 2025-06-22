from dataclasses import dataclass
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ClientAction(str, Enum):
    pass


def CreateButton(cb: type[CallbackData], action: ClientAction) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=cb(action=action).pack(),
    )



@dataclass
class Menu:
    text: str
    reply_markup: InlineKeyboardMarkup | None
