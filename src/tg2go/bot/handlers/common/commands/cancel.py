from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from tg2go.bot.lib.message.io import SendMessage

router = Router()


@router.message(Command("cancel"))
async def CommandCancel(message: types.Message, state: FSMContext) -> None:
    """
    Handles the /cancel command, allowing users to cancel ongoing interactions
    and removing any active reply keyboards. It also clears the user's state.
    """
    await SendMessage(
        chat_id=message.chat.id,
        text="Canceled",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await state.clear()
