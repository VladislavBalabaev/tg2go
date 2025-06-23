from aiogram import F, Router, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.category_action.change import (
    CategoryChangeAction,
    CategoryChangeCallbackData,
    CategoryChangeMenu,
)
from tg2go.bot.lib.message.io import ContextIO, SendMessage
from tg2go.db.models.category import Category
from tg2go.services.staff.category import StaffCategoryService

router = Router()


class CategoryChangeNameStates(StatesGroup):
    Change = State()


@router.callback_query(
    CategoryChangeCallbackData.filter(F.action == CategoryChangeAction.Name)
)
async def CategoryChangeName(
    callback_query: types.CallbackQuery,
    callback_data: CategoryChangeCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await state.set_data({"category_id": callback_data.category_id})

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите новое название категории",
    )

    await state.set_state(CategoryChangeNameStates.Change)


@router.message(StateFilter(CategoryChangeNameStates.Change), F.content_type == "text")
async def CategoryChangeNameChange(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    data = await state.get_data()

    srv = StaffCategoryService.Create()
    await srv.UpdateCategory(
        category_id=data["category_id"],
        column=Category.name,
        value=message.text,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Название категории успешно изменено",
    )

    menu = await CategoryChangeMenu(data["category_id"])
    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await state.clear()


class CategoryChangeIndexStates(StatesGroup):
    Change = State()


@router.callback_query(
    CategoryChangeCallbackData.filter(F.action == CategoryChangeAction.Index)
)
async def CategoryChangeIndex(
    callback_query: types.CallbackQuery,
    callback_data: CategoryChangeCallbackData,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await state.set_data({"category_id": callback_data.category_id})

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите новый индекс категории",
    )

    await state.set_state(CategoryChangeIndexStates.Change)


@router.message(StateFilter(CategoryChangeIndexStates.Change), F.content_type == "text")
async def CategoryChangeIndexChange(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    if not message.text.isdigit():
        await SendMessage(
            chat_id=message.chat.id,
            text="Индекс категории обязан быть целым положительным числом",
            context=ContextIO.UserFailed,
        )
        return

    data = await state.get_data()

    srv = StaffCategoryService.Create()
    await srv.UpdateCategory(
        category_id=data["category_id"],
        column=Category.index,
        value=int(message.text),
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Индекс категории успешно изменен",
    )

    menu = await CategoryChangeMenu(data["category_id"])
    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await state.clear()


@router.callback_query(
    CategoryChangeCallbackData.filter(F.action == CategoryChangeAction.Back)
)
async def CategoryChangeBack(
    callback_query: types.CallbackQuery,
    callback_data: CategoryChangeCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CategoryMenu(callback_data.category_id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
