from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import StaffAction, StaffMenu, StaffPosition
from tg2go.bot.lib.message.image import GetGoodImageDir
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


async def GoodRemoveMenu(good_id: GoodId) -> StaffMenu:
    good_srv = StaffGoodService.Create()
    good = await good_srv.GetGood(good_id)

    text = f"🔴 Бот не работает\n\nО позиции:\n{good.GetStaffInfo()}{StaffPosition.Good(good)}"

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

    return StaffMenu(
        image_dir=GetGoodImageDir(good.good_id),
        caption=text,
        reply_markup=markup,
    )
