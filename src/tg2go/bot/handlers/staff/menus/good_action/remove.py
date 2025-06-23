from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from tg2go.bot.handlers.staff.menus.common import MediaMenu, StaffAction, StaffPosition
from tg2go.db.models.common.types import GoodId
from tg2go.services.staff.good import StaffGoodService


class GoodRemoveAction(StaffAction):
    Delete = "🗑️ Точно удалить"
    Back = "⬅️ Назад"


class GoodRemoveCallbackData(CallbackData, prefix="staff.good.remove"):
    action: GoodRemoveAction
    good_id: GoodId


def CreateButton(action: StaffAction, good_id: GoodId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=GoodRemoveCallbackData(
            action=action,
            good_id=good_id,
        ).pack(),
    )


async def GoodRemoveMenu(good_id: GoodId) -> MediaMenu:
    good_srv = StaffGoodService.Create()
    good = await good_srv.GetGood(good_id)

    text = f"🔴 Бот не работает\n\nО позиции:\n{good.GetInfoForStaff()}{StaffPosition.Good(good)}"
    media = InputMediaPhoto(media=good.image_file_id, caption=text, parse_mode="HTML")

    buttons = [
        [
            CreateButton(
                action=GoodRemoveAction.Delete,
                good_id=good_id,
            )
        ],
        [
            CreateButton(
                action=GoodRemoveAction.Back,
                good_id=good_id,
            ),
        ],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return MediaMenu(
        media=media,
        reply_markup=markup,
    )
