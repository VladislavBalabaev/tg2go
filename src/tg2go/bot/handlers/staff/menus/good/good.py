from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg2go.bot.handlers.staff.menus.common import StaffAction, StaffMenu, StaffPosition
from tg2go.bot.lib.message.image import GetGoodImageDir
from tg2go.db.models.common.types import GoodId
from tg2go.services.staff.good import StaffGoodService


class GoodAction(StaffAction):
    Change = "✏️ Изменить позицию"
    Remove = "🗑️ Удалить позицию"
    Enable = "🚀 Сделать доступным"
    Disable = "💤 Сделать недоступным"
    Back = "⬅️ Назад"


class GoodCallbackData(CallbackData, prefix="staff.good"):
    action: GoodAction
    good_id: GoodId


def CreateButton(action: StaffAction, good_id: GoodId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=GoodCallbackData(
            action=action,
            good_id=good_id,
        ).pack(),
    )


async def GoodMenu(good_id: GoodId) -> StaffMenu:
    good_srv = StaffGoodService.Create()
    good = await good_srv.GetGood(good_id)

    available_action = GoodAction.Disable if good.available else GoodAction.Enable

    text = f"🔴 Бот не работает\n\n{good.GetStaffInfo()}{StaffPosition.Good(good)}"
    buttons = [
        [
            CreateButton(
                action=GoodAction.Change,
                good_id=good_id,
            ),
            CreateButton(
                action=GoodAction.Remove,
                good_id=good_id,
            ),
        ],
        [
            CreateButton(
                action=available_action,
                good_id=good_id,
            ),
        ],
        [
            CreateButton(
                action=GoodAction.Back,
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
