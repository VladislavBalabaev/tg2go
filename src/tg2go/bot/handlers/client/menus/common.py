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
from tg2go.db.models.order_item import OrderItem
from tg2go.services.client.order import ClientOrderService


class ClientAction(str, Enum):
    pass


@dataclass
class ClientMenu:
    image_dir: Path
    caption: str
    reply_markup: types.InlineKeyboardMarkup | None


class ClientPosition:
    start = "\n\n\n➤ "

    class Label(str, Enum):
        Menu = "Меню"
        Cart = "Корзина"

    @classmethod
    def _Path(cls, *args: str) -> str:
        parts = [f"[{i}]" for i in args]

        return cls.start + " > ".join(parts)

    @classmethod
    def Hub(cls) -> str:
        return cls._Path(cls.Label.Menu.value)

    @classmethod
    def Category(cls, category: Category) -> str:
        return cls._Path(cls.Label.Menu.value, category.name)

    @classmethod
    def Good(cls, good: Good) -> str:
        return cls._Path(cls.Label.Menu.value, good.category.name, good.name)

    @classmethod
    def Item(cls, item: OrderItem) -> str:
        return cls._Path(cls.Label.Menu.value, item.good.category.name, item.good.name)

    @classmethod
    def Cart(cls) -> str:
        return cls._Path(cls.Label.Cart.value)

    @classmethod
    def CartItem(cls, item: OrderItem) -> str:
        return cls._Path(cls.Label.Cart.value, item.good.name)


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


async def SendClientMenu(chat_id: int, menu: ClientMenu) -> types.Message | None:
    srv = await ClientOrderService.Create(chat_id)
    await srv.DeleteOrderMessage()

    message = await SendImage(
        chat_id=chat_id,
        image_dir=menu.image_dir,
        caption=menu.caption,
        reply_markup=menu.reply_markup,
    )

    if not message:
        logging.error(f"Can't send menu to chat_id={chat_id}")
        return None

    await srv.SetOrderMessage(message.message_id)

    return message


async def ChangeToNewClientMenu(
    callback_query: types.CallbackQuery,
    new_menu: ClientMenu,
) -> None:
    msg = callback_query.message
    assert isinstance(msg, types.Message)

    image = Image(new_menu.image_dir)
    media = types.InputMediaPhoto(
        media=image.GetFileId(),
        caption=new_menu.caption,
        parse_mode="HTML",
    )

    try:
        await msg.edit_media(
            media=media,
            reply_markup=new_menu.reply_markup,
        )
    except (TelegramNetworkError, TelegramBadRequest) as e:
        logging.info(
            f"file_id={image.GetFileId()} is expired. Sending raw image. Error: {e}"
        )

        media.media = image.GetSource()

        updated = await msg.edit_media(
            media=media,
            reply_markup=new_menu.reply_markup,
        )

        if isinstance(updated, types.Message) and updated.photo:
            image.UpdateFileId(updated.photo[-1].file_id)

    part = await GetChatUserLoggingPart(msg.chat.id)
    logging.info(
        f"{part} {SignIO.Out.value}{ContextIO.Doc.value} {repr(media.caption)}"
    )
