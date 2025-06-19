from aiogram import F, Router, types

from tg2go.bot.handlers.staff.common import (
    StaffAction,
    StaffCallbackData,
    StaffHeaderText,
    StaffKeyboard,
    StaffMenu,
)

router = Router()


def StaffMenuCategory(chat_id: int) -> StaffMenu:
    return StaffMenu(
        text=StaffHeaderText.Category,
        reply_markup=StaffKeyboard(
            actions=[
                StaffAction.AddCategory,
                StaffAction.RemoveCategory,
                StaffAction.RenameCategory,
                StaffAction.Cancel,
            ],
            chat_id=chat_id,
        ),
    )


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.Categories))
async def CommandStaffCategories(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = StaffMenuCategory(callback_query.message.chat.id)

    await callback_query.message.edit_text(
        text=menu.text,
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.AddCategory))
async def CommandStaffAddCategory(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None: ...


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.RemoveCategory))
async def CommandStaffRemoveCategory(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None: ...


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.RenameCategory))
async def CommandStaffRenameCategory(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None: ...
