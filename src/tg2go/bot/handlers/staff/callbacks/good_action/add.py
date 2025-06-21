from decimal import Decimal, InvalidOperation

from aiogram import F, Router, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.lib.message.io import ContextIO, SendMessage
from tg2go.services.staff.good import StaffGoodService

router = Router()


class AddGoodStates(StatesGroup):
    name = State()
    price_rub = State()
    description = State()
    image_url = State()


@router.message(StateFilter(AddGoodStates.name), F.content_type == "text")
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

    await state.set_state(AddGoodStates.price_rub)


@router.message(StateFilter(AddGoodStates.price_rub), F.content_type == "text")
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
                text="Индекс обязян быть целым положительным числом",
                context=ContextIO.UserFailed,
            )
            return

    data = await state.get_data()
    data.update({"price_rub": price_rub})
    await state.set_data(data)

    await SendMessage(
        chat_id=message.chat.id,
        text="Укажите описание продукта, добавляя ингридиенты и граммовки.",
    )

    await state.set_state(AddGoodStates.description)


@router.message(StateFilter(AddGoodStates.description), F.content_type == "text")
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
        text="kiday pape url fotochki",
    )

    await state.set_state(AddGoodStates.image_url)


@router.message(StateFilter(AddGoodStates.image_url), F.content_type == "text")
async def CommandStaffAddGoodImageUrl(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()
    data.update({"image_url": message.text})

    srv = StaffGoodService.Create()
    await srv.InsertNewGood(**data)

    await SendMessage(
        chat_id=message.chat.id,
        text="Новый продукт в категории успешно создан",
    )

    menu = await CategoryMenu(data["category_id"])
    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await state.clear()
