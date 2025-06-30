from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from tg2go.bot.handlers.staff.callbacks.category.add import AddCategoryStates
from tg2go.bot.handlers.staff.menus.category.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.common import staff_menu
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
        text="Категории нужны для логической группировки товаров и задают структуру меню. Каждой категории присваивается числовой индекс, который определяет её позицию относительно других: чем больше индекс, тем дальше категория в списке категорий.\n\nПример\nДопустим, есть три категории:\n•A (индекс 5)\n•B (индекс 1)\n•C (индекс 7)\n\nВ меню они отобразятся в порядке B -> A -> C, поскольку 1 < 5 < 7.",
    )
    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Напишите название новой категории.\nПомните, оно должно быть коротким",
    )

    await state.set_state(AddCategoryStates.Name)


@router.callback_query(SettingsCategoryCallbackData.filter())
async def SettingsCategory(
    callback_query: types.CallbackQuery,
    callback_data: SettingsCategoryCallbackData,
) -> None:
    await staff_menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await CategoryMenu(callback_data.category_id),
    )
    await callback_query.answer()


@router.callback_query(SettingsCallbackData.filter(F.action == SettingsAction.Main))
async def SettingsMain(callback_query: types.CallbackQuery) -> None:
    await staff_menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=PanelMenu(),
    )
    await callback_query.answer()
