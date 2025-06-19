from aiogram import F, Router, types

from tg2go.bot.handlers.staff.common import (
    StaffAction,
    StaffCallbackData,
    StaffHeaderText,
    StaffKeyboard,
    StaffMenu,
)
from tg2go.bot.lifecycle.active import bot_state

router = Router()


def StaffMenuSettings(chat_id: int) -> StaffMenu:
    if bot_state.active:
        text = StaffHeaderText.Active
    else:
        text = StaffHeaderText.Inactive

    return StaffMenu(
        text=text,
        reply_markup=StaffKeyboard(
            actions=[StaffAction.Categories, StaffAction.Goods, StaffAction.Cancel],
            chat_id=chat_id,
        ),
    )


@router.callback_query(StaffCallbackData.filter(F.action == StaffAction.Settings))
async def CommandStaffSettings(
    callback_query: types.CallbackQuery,
    callback_data: StaffCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    menu = StaffMenuSettings(callback_query.message.chat.id)

    await callback_query.message.edit_reply_markup(
        reply_markup=menu.reply_markup,
    )
    await callback_query.answer()
