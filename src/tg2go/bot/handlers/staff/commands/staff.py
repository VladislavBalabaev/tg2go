from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.handlers.staff.menus.staff import StaffMenu
from tg2go.bot.lib.message.filters import StaffFilter
from tg2go.bot.lib.message.io import SendMessage

router = Router()


@router.message(Command("staff"), StateFilter(None), StaffFilter())
async def CommandStaff(message: types.Message) -> None:
    menu = StaffMenu(message.chat.id)

    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
