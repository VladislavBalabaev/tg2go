from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from tg2go.bot.handlers.staff.callbacks.category_action.add import AddCategoryStates
from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.panel import PanelMenu
from tg2go.bot.handlers.staff.menus.settings import (
    SettingsAction,
    SettingsCallbackData,
    SettingsCategoryCallbackData,
)
from tg2go.bot.lib.message.io import SendMessage

router = Router()


@router.callback_query(
    SettingsCallbackData.filter(F.action == SettingsAction.AddCategory)
)
async def SettingsAddCategory(
    callback_query: types.CallbackQuery,
    state: FSMContext,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Категория нужна для группировки позиций ассортимента.\nПрисваиваемый категории индекс отвечает за позицию категории относительно других.\nЧем больше индекс, тем ниже категория в списке.\n\nПример:\n(имя=A, индекс=5), (имя=B, индекс=1), (имя=C, индекс=7)\nбудут идти как\nB\nA\nC",
    )
    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите название новой категории.\nПомните, оно должно быть коротким",
    )

    await state.set_state(AddCategoryStates.name)


@router.callback_query(SettingsCategoryCallbackData.filter())
async def SettingsCategory(
    callback_query: types.CallbackQuery,
    callback_data: SettingsCategoryCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CategoryMenu(callback_data.category_id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(SettingsCallbackData.filter(F.action == SettingsAction.Back))
async def SettingsBack(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = PanelMenu()

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
