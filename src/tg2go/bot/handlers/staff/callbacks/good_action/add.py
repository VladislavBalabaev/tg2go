from decimal import Decimal, InvalidOperation

from aiogram import F, Router, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.lib.message.file import DownloadImage
from tg2go.bot.lib.message.io import ContextIO, SendMessage
from tg2go.services.staff.good import StaffGoodService

router = Router()


class AddGoodStates(StatesGroup):
    Name = State()
    PriceRub = State()
    Description = State()
    ImageUrl = State()


@router.message(StateFilter(AddGoodStates.Name), F.content_type == "text")
async def CommandStaffAddGoodName(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()
    data.update({"name": message.text})
    await state.set_data(data)

    await SendMessage(
        chat_id=message.chat.id,
        text="Укажите цену в рублях числом в формате `123` или `123.45`",
    )

    await state.set_state(AddGoodStates.PriceRub)


@router.message(StateFilter(AddGoodStates.PriceRub), F.content_type == "text")
async def CommandStaffAddGoodPriceRub(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    try:
        price_rub = Decimal(message.text)
    except (InvalidOperation, ValueError):
        if not message.text.isdigit():
            await SendMessage(
                chat_id=message.chat.id,
                text="❌ Цена обязана быть в числовом формате `123` или `123.45`",
                context=ContextIO.UserFailed,
            )
            return

    data = await state.get_data()
    data.update({"price_rub": price_rub})
    await state.set_data(data)

    await SendMessage(
        chat_id=message.chat.id,
        text="Укажите описание продукта, добавляя ингредиенты и граммовки.",
    )

    await state.set_state(AddGoodStates.Description)


@router.message(StateFilter(AddGoodStates.Description), F.content_type == "text")
async def CommandStaffAddGoodDescription(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()
    data.update({"description": message.text})
    await state.set_data(data)

    await SendMessage(
        chat_id=message.chat.id,
        text="Отправьте фотографию для новой позиции в меню",
    )

    await state.set_state(AddGoodStates.ImageUrl)


@router.message(StateFilter(AddGoodStates.ImageUrl))
async def CommandStaffAddGoodImageUrl(
    message: types.Message,
    state: FSMContext,
) -> None:
    if message.photo is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Вы отправили не фото для создаваемой позиции.\n\nОтправьте, пожалуйста, фотографию для новой позиции в меню",
            context=ContextIO.UserFailed,
        )
        return

    photo = message.photo[-1]

    await DownloadImage(photo)

    data = await state.get_data()
    data.update({"image_file_id": photo.file_id})

    srv = StaffGoodService.Create()
    await srv.InsertNewGood(**data)

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Новая позиция в категории успешно создана",
    )

    menu = await CategoryMenu(data["category_id"])
    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await state.clear()
