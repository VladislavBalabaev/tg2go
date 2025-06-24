import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from aiogram import types
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError

from tg2go.bot.lib.chat.username import GetChatUserLoggingPart
from tg2go.bot.lib.message.image import Image
from tg2go.bot.lib.message.io import ContextIO, SendImage, SignIO
from tg2go.db.models.category import Category
from tg2go.db.models.good import Good


class StaffAction(str, Enum):
    pass


@dataclass
class Menu:
    image_dir: Path
    caption: str
    reply_markup: types.InlineKeyboardMarkup | None


class StaffPosition:
    start = "\n\n\n🔹"

    class Label(str, Enum):
        Settings = "Настройки"

    @classmethod
    def _Path(cls, *args: str) -> str:
        parts = [f"[{i}]" for i in args]

        return cls.start + " > ".join(parts)

    @classmethod
    def Settings(cls) -> str:
        return cls._Path(cls.Label.Settings.value)

    @classmethod
    def Category(cls, category: Category) -> str:
        return cls._Path(cls.Label.Settings.value, category.name)

    @classmethod
    def Good(cls, good: Good) -> str:
        return cls._Path(cls.Label.Settings.value, good.category.name, good.name)


def SplitButtonsInTwoColumns(
    plain_buttons: list[types.InlineKeyboardButton],
) -> list[list[types.InlineKeyboardButton]]:
    new_buttons = []

    group = []
    for i, button in enumerate(plain_buttons):
        group.append(button)

        if i % 2 == 1:
            new_buttons.append(group)
            group = []

    if group:
        new_buttons.append(group)

    return new_buttons


async def SendMenu(chat_id: int, menu: Menu) -> types.Message | None:
    # TODO: make a singleton staff image among chat ids

    return await SendImage(
        chat_id=chat_id,
        image_dir=menu.image_dir,
        caption=menu.caption,
        reply_markup=menu.reply_markup,
    )


async def ChangeToNewMenu(
    callback_query: types.CallbackQuery,
    new_menu: Menu,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    image = Image(new_menu.image_dir)

    media = types.InputMediaPhoto(
        media=image.GetFileId(),
        caption=new_menu.caption,
        parse_mode="HTML",
    )

    try:
        await callback_query.message.edit_media(
            media=media,
            reply_markup=new_menu.reply_markup,
        )
    except (TelegramNetworkError, TelegramBadRequest) as e:
        logging.error(e)
        logging.info(f"file_id={image.GetFileId()} is expired. Sending raw image.")

        media.media = image.GetSource()

        message = await callback_query.message.edit_media(
            media=media,
            reply_markup=new_menu.reply_markup,
        )

        assert isinstance(message, types.Message)
        assert isinstance(message.photo, list)
        image.UpdateFileId(message.photo[-1].file_id)

    part = await GetChatUserLoggingPart(callback_query.message.chat.id)
    logging.info(
        f"{part} {SignIO.Out.value}{ContextIO.Doc.value} {repr(media.caption)}"
    )
