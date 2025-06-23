from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from tg2go.bot.handlers.staff.menus.common import MediaMenu, StaffAction, StaffPosition
from tg2go.db.models.common.types import GoodId
from tg2go.services.staff.good import StaffGoodService


class GoodChangeAction(StaffAction):
    Name = "✏️ Изменить название"
    PriceRub = "✏️ Изменить цену"
    Description = "✏️ Изменить описание"
    ImageUrl = "✏️ Изменить картинку"
    Back = "⬅️ Назад"


class GoodChangeCallbackData(CallbackData, prefix="staff.good.change"):
    action: GoodChangeAction
    good_id: GoodId


def CreateButton(action: StaffAction, good_id: GoodId) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=action.value,
        callback_data=GoodChangeCallbackData(
            action=action,
            good_id=good_id,
        ).pack(),
    )


async def GoodChangeMenu(good_id: GoodId) -> MediaMenu:
    good_srv = StaffGoodService.Create()
    good = await good_srv.GetGood(good_id)

    text = f"🔴 Бот не работает\n\nО позиции:\n{good.GetInfoForStaff()}{StaffPosition.Good(good)}"
    media = InputMediaPhoto(media=good.image_file_id, caption=text, parse_mode="HTML")

    buttons = [
        [
            CreateButton(
                action=GoodChangeAction.Name,
                good_id=good_id,
            )
        ],
        [
            CreateButton(
                action=GoodChangeAction.PriceRub,
                good_id=good_id,
            )
        ],
        [
            CreateButton(
                action=GoodChangeAction.Description,
                good_id=good_id,
            )
        ],
        [
            CreateButton(
                action=GoodChangeAction.ImageUrl,
                good_id=good_id,
            )
        ],
        [
            CreateButton(
                action=GoodChangeAction.Back,
                good_id=good_id,
            ),
        ],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return MediaMenu(
        media=media,
        reply_markup=markup,
    )
