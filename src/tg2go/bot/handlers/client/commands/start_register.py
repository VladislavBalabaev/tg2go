from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from tg2go.bot.handlers.client.commands.start_order import SendPanelMenu
from tg2go.bot.lib.message.io import ContextIO, SendDocument, SendMessage
from tg2go.core.configs.paths import PATH_TERMS
from tg2go.db.models.user import User
from tg2go.services.client.order import CreateNewOrder
from tg2go.services.user import UserService

router = Router()

# TODO: add bot's: picture, about, description, description picture


class StartStates(StatesGroup):
    GetPhoneNumber = State()
    Terms = State()


@router.message(StateFilter(None), Command("start"))
async def CommandStart(message: types.Message, state: FSMContext) -> None:
    button = KeyboardButton(text="📱 Поделиться контактом", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

    await SendMessage(
        chat_id=message.chat.id,
        text="Пожалуйста, поделитесь с нами своим контактом\n\nЕсли меню с кнопками скрыто, нажмите на значок 🎛 в правом нижнем углу",
        reply_markup=keyboard,
    )

    await state.set_state(StartStates.GetPhoneNumber)


@router.message(StateFilter(StartStates.GetPhoneNumber))
async def CommandStartGetPhoneNumber(message: types.Message, state: FSMContext) -> None:
    if message.contact is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Пожалуйста, отправьте свой номер телефона, используя кнопку ниже.\n\nЕсли меню с кнопками скрыто, нажмите на значок 🎛 в правом нижнем углу",
            context=ContextIO.UserFailed,
        )
        return

    if message.contact.user_id is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Не удалось получить ваш номер телефона, так как вы не являетесь пользователем Telegram.\nПожалуйста, попробуйте снова из своего пользовательского профиля",
            context=ContextIO.UserFailed,
        )
        return

    if message.contact.user_id != message.chat.id:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Вы отправили чужой номер телефона.\nПожалуйста, отправьте свой собственный номер.\n\nЕсли меню с кнопками скрыто, нажмите на значок 🎛 в правом нижнем углу",
            context=ContextIO.UserFailed,
        )
        return

    srv = UserService.Create()
    await srv.UpdateUser(
        chat_id=message.chat.id,
        column=User.phone_number,
        value=message.contact.phone_number,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Спасибо!",
        reply_markup=ReplyKeyboardRemove(),
    )

    button = KeyboardButton(text="📄 Да, я принимаю")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

    # TODO: create actual terms of service
    await SendDocument(
        chat_id=message.chat.id,
        document=types.FSInputFile(PATH_TERMS),
        caption="Ознакомьтесь с условиями Пользовательского соглашения и подтвердите своё согласие на обработку персональных данных, нажав на кнопку 📄 Да, я принимаю\n\nЕсли меню с кнопками скрыто, нажмите на значок 🎛 в правом нижнем углу",
        reply_markup=keyboard,
    )

    await state.set_state(StartStates.Terms)
    await state.set_data({"button_text": button.text})


@router.message(StateFilter(StartStates.Terms), F.content_type == "text")
async def CommandStartTerms(message: types.Message, state: FSMContext) -> None:
    assert message.text is not None

    data = await state.get_data()
    button_text = data["button_text"]

    if message.text != button_text:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Пожалуйста, подтвердите согласие с Условиями, нажав на кнопку 📄 Да, я принимаю\nБез этого вы не можете пользоваться сервисом.\n\nЕсли меню с кнопками скрыто, нажмите на значок 🎛 в правом нижнем углу",
            context=ContextIO.UserFailed,
        )
        return

    srv = UserService.Create()
    await srv.UpdateUser(
        chat_id=message.chat.id,
        column=User.verified,
        value=True,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Спасибо!",
        reply_markup=ReplyKeyboardRemove(),
    )

    await CreateNewOrder(message.chat.id)
    await SendPanelMenu(message)

    await state.clear()
