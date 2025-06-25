from aiogram import F, Router, types

from tg2go.bot.handlers.staff.menus.category import CategoryMenu
from tg2go.bot.handlers.staff.menus.category_action.remove import (
    CategoryRemoveAction,
    CategoryRemoveCallbackData,
)
from tg2go.bot.handlers.staff.menus.common import menu
from tg2go.bot.handlers.staff.menus.settings import SettingsMenu
from tg2go.services.staff.category import StaffCategoryService

router = Router()


@router.callback_query(
    CategoryRemoveCallbackData.filter(F.action == CategoryRemoveAction.Delete)
)
async def CategoryRemoveDelete(
    callback_query: types.CallbackQuery,
    callback_data: CategoryRemoveCallbackData,
) -> None:
    srv = StaffCategoryService.Create()
    await srv.InvalidateCategory(callback_data.category_id)

    await menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await SettingsMenu(),
    )
    await callback_query.answer()


@router.callback_query(
    CategoryRemoveCallbackData.filter(F.action == CategoryRemoveAction.Back)
)
async def CategoryRemoveBack(
    callback_query: types.CallbackQuery,
    callback_data: CategoryRemoveCallbackData,
) -> None:
    await menu.ChangeToNewMenu(
        callback_query=callback_query,
        new_menu=await CategoryMenu(callback_data.category_id),
    )
    await callback_query.answer()
