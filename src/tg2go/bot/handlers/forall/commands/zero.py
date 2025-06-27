from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from tg2go.bot.lib.message.io import ContextIO, SendMessage

router = Router()


@router.message(F.content_type == "text")
async def ZeroMessageText(message: types.Message) -> None:
    await SendMessage(
        chat_id=message.chat.id,
        text="Сейчас вы не выполняете команду.\nВыберите что-то из меню",
        context=ContextIO.ZeroMessage,
    )


@router.message()
async def NoTextMessage(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        text = "Бот работает только с текстовыми сообщениями.\nВыберите что-то из меню"
    else:
        text = "Бот работает только с текстовыми сообщениями\nПопробуйте снова"

    await SendMessage(chat_id=message.chat.id, text=text, context=ContextIO.NoText)
