from decimal import Decimal, InvalidOperation

from aiogram import F, Router, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.handlers.staff.menus.good import GoodMenu
from tg2go.bot.handlers.staff.menus.good_action.change import (
    GoodChangeAction,
    GoodChangeCallbackData,
    GoodChangeMenu,
)
from tg2go.bot.lib.message.file import DownloadImage
from tg2go.bot.lib.message.io import ContextIO, SendMessage
from tg2go.bot.lifecycle.creator import bot
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

    menu = await GoodChangeMenu(data["good_id"])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=menu.media.media,
        caption=menu.media.caption,
        reply_markup=menu.reply_markup,
    )

    await state.clear()


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
        text="Напишите новою цену позиции",
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

    menu = await GoodChangeMenu(data["good_id"])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=menu.media.media,
        caption=menu.media.caption,
        reply_markup=menu.reply_markup,
    )

    await state.clear()


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

    menu = await GoodChangeMenu(data["good_id"])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=menu.media.media,
        caption=menu.media.caption,
        reply_markup=menu.reply_markup,
    )

    await state.clear()


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
            text="❌ Вы отправили не фото для создаваемой позиции.\n\nОтправьте, пожалуйста, фотографию для новой позиции в меню",
            context=ContextIO.UserFailed,
        )
        return

    data = await state.get_data()

    photo = message.photo[-1]
    await DownloadImage(photo)

    srv = StaffGoodService.Create()
    await srv.UpdateGood(
        good_id=data["good_id"],
        column=Good.image_file_id,
        value=photo.file_id,
    )
    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Новое фото позиции установлено",
    )

    menu = await GoodChangeMenu(data["good_id"])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=menu.media.media,
        caption=menu.media.caption,
        reply_markup=menu.reply_markup,
    )

    await state.clear()


@router.callback_query(GoodChangeCallbackData.filter(F.action == GoodChangeAction.Back))
async def GoodChangeBack(
    callback_query: types.CallbackQuery,
    callback_data: GoodChangeCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await GoodMenu(callback_data.good_id)

    await callback_query.message.edit_media(
        media=menu.media,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
