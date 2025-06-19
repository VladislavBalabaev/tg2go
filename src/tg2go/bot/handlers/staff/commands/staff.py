from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.handlers.staff.callbacks.mainmenu import StaffMainMenu
from tg2go.bot.lib.message.filters import StaffFilter
from tg2go.bot.lib.message.io import SendMessage

router = Router()


@router.message(Command("staff"), StateFilter(None), StaffFilter())
async def CommandStaff(message: types.Message) -> None:
    menu = StaffMainMenu(message.chat.id)

    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
