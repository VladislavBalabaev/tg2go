from aiogram import F, Router, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg2go.bot.handlers.staff.menus.settings import SettingsMenu
from tg2go.bot.lib.message.io import ContextIO, SendMessage
from tg2go.services.staff.category import StaffCategoryService

router = Router()


class AddCategoryStates(StatesGroup):
    Name = State()
    Index = State()


@router.message(StateFilter(AddCategoryStates.Name), F.content_type == "text")
async def CommandStaffAddCategoryName(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    await state.set_data({"name": message.text})

    await SendMessage(
        chat_id=message.chat.id,
        text="Присвойте индекс категории (целым положительным числом).\nЧем выше число, тем ниже по списку будет категория",
    )

    await state.set_state(AddCategoryStates.Index)


@router.message(StateFilter(AddCategoryStates.Index), F.content_type == "text")
async def CommandStaffAddCategoryIndex(
    message: types.Message,
    state: FSMContext,
) -> None:
    assert message.text is not None

    if not message.text.isdigit():
        await SendMessage(
            chat_id=message.chat.id,
            text="Индекс обязан быть целым положительным числом",
            context=ContextIO.UserFailed,
        )
        return

    data = await state.get_data()

    srv = StaffCategoryService.Create()
    await srv.InsertNewCategory(
        name=str(data["name"]),
        index=int(message.text),
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Новая категория успешно создана",
    )

    menu = await SettingsMenu()
    await SendMessage(
        chat_id=message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )

    await state.clear()
