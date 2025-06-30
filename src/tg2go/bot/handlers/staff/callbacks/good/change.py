from decimal import Decimal, InvalidOperation

from aiogram import F, Router, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.handlers.staff.menus.common import staff_menu
from tg2go.bot.handlers.staff.menus.good.change import (
    GoodChangeAction,
    GoodChangeCallbackData,
    GoodChangeMenu,
)
from tg2go.bot.handlers.staff.menus.good.good import GoodMenu
from tg2go.bot.lib.message.image import GetGoodImageDir, Image
from tg2go.bot.lib.message.io import ContextIO, SendMessage
from tg2go.db.models.good import Good
from tg2go.services.staff.good import StaffGoodService

router = Router()


class GoodChangeNameStates(StatesGroup):
    Change = State()


@router.callback_query(GoodChangeCallbackData.filter(F.action == GoodChangeAction.Name))
async def GoodChangeName(
    callback_query: types.CallbackQuery,
    callback_data: GoodChangeCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await state.set_data({"good_id": callback_data.good_id})

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите новое название позиции",
    )

    await state.set_state(GoodChangeNameStates.Change)


@router.message(StateFilter(GoodChangeNameStates.Change), F.content_type == "text")
async def GoodChangeNameChange(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()

    srv = StaffGoodService.Create()
    await srv.UpdateGood(
        good_id=data["good_id"],
        column=Good.name,
        value=message.text,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Название позиции успешно изменено",
    )
    await state.clear()

    await staff_menu.SendMenu(
        chat_id=message.chat.id,
        menu=await GoodChangeMenu(data["good_id"]),
    )


class GoodChangePriceRubStates(StatesGroup):
    Change = State()


@router.callback_query(
    GoodChangeCallbackData.filter(F.action == GoodChangeAction.PriceRub)
)
async def GoodChangePriceRub(
    callback_query: types.CallbackQuery,
    callback_data: GoodChangeCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await state.set_data({"good_id": callback_data.good_id})

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите новую цену позиции",
    )

    await state.set_state(GoodChangePriceRubStates.Change)


@router.message(StateFilter(GoodChangePriceRubStates.Change), F.content_type == "text")
async def GoodChangePriceRubChange(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()

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

    srv = StaffGoodService.Create()
    await srv.UpdateGood(
        good_id=data["good_id"],
        column=Good.price_rub,
        value=price_rub,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Цена позиции успешно изменена",
    )
    await state.clear()

    await staff_menu.SendMenu(
        chat_id=message.chat.id,
        menu=await GoodChangeMenu(data["good_id"]),
    )


class GoodChangeDescriptionStates(StatesGroup):
    Change = State()


@router.callback_query(
    GoodChangeCallbackData.filter(F.action == GoodChangeAction.Description)
)
async def GoodChangeDescription(
    callback_query: types.CallbackQuery,
    callback_data: GoodChangeCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await state.set_data({"good_id": callback_data.good_id})

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите новое описание позиции",
    )

    await state.set_state(GoodChangeDescriptionStates.Change)


@router.message(
    StateFilter(GoodChangeDescriptionStates.Change), F.content_type == "text"
)
async def GoodChangeDescriptionChange(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()

    srv = StaffGoodService.Create()
    await srv.UpdateGood(
        good_id=data["good_id"],
        column=Good.description,
        value=message.text,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Описание позиции успешно изменено",
    )
    await state.clear()

    await staff_menu.SendMenu(
        chat_id=message.chat.id,
        menu=await GoodChangeMenu(data["good_id"]),
    )


class GoodChangeImageUrlStates(StatesGroup):
    Change = State()


@router.callback_query(
    GoodChangeCallbackData.filter(F.action == GoodChangeAction.ImageUrl)
)
async def GoodChangeImageUrl(
    callback_query: types.CallbackQuery,
    callback_data: GoodChangeCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await state.set_data({"good_id": callback_data.good_id})

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Отправьте новое фото позиции",
    )

    await state.set_state(GoodChangeImageUrlStates.Change)


@router.message(StateFilter(GoodChangeImageUrlStates.Change))
async def GoodChangeImageUrlChange(
    message: types.Message,
    state: FSMContext,
) -> None:
    if message.photo is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Вы отправили не фото для позиции.\n\nОтправьте, пожалуйста, новое фото позиции",
            context=ContextIO.UserFailed,
        )
        return

    data = await state.get_data()

    image = Image(GetGoodImageDir(data["good_id"]))
    await image.DownloadSource(message.photo[-1])

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Новое фото позиции установлено",
    )
    await state.clear()

    await staff_menu.SendMenu(
        chat_id=message.chat.id,
        menu=await GoodChangeMenu(data["good_id"]),
    )


@router.callback_query(GoodChangeCallbackData.filter(F.action == GoodChangeAction.Back))
async def GoodChangeBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodChangeCallbackData,
) -> None:
    await staff_menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await GoodMenu(callback_data.good_id),
    )
    await callback_query.answer()
