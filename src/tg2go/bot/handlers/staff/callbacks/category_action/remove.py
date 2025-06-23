from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.category_action.remove import (
    CategoryRemoveAction,
    CategoryRemoveCallbackData,
)
from tg2go.bot.handlers.staff.menus.settings import SettingsMenu
from tg2go.bot.lib.message.io import SendMessage
from tg2go.services.staff.category import StaffCategoryService

router = Router()


@router.callback_query(
    CategoryRemoveCallbackData.filter(F.action == CategoryRemoveAction.Delete)
)
async def CategoryRemoveDelete(
    callback_query: types.CallbackQuery,
    callback_data: CategoryRemoveCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

    srv = StaffCategoryService.Create()
    await srv.InvalidateCategory(callback_data.category_id)

    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text="Категория успешно удалена",
    )

    menu = await SettingsMenu()
    await SendMessage(
        chat_id=callback_query.message.chat.id,
        text=menu.text,
        reply_markup=menu.reply_markup,
    )


@router.callback_query(
    CategoryRemoveCallbackData.filter(F.action == CategoryRemoveAction.Back)
)
async def CategoryRemoveBack(
    callback_query: types.CallbackQuery,
    callback_data: CategoryRemoveCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = await CategoryMenu(callback_data.category_id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
