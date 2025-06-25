from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from tg2go.bot.handlers.staff.menus.common import menu
from tg2go.bot.handlers.staff.menus.panel import PanelMenu
from tg2go.bot.lib.message.filter import StaffFilter

router = Router()


@router.message(Command("staff"), StateFilter(None), StaffFilter())
async def CommandStaff(message: types.Message) -> None:
    await menu.SendMenu(chat_id=message.chat.id, menu=PanelMenu())
