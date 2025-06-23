import json
import os
from typing import Any

from aiogram import types

from tg2go.bot.lib.message.io import SendDocument
from tg2go.bot.lifecycle.creator import bot
from tg2go.core.configs.paths import DIR_IMAGES, DIR_TEMP


def ToJSONText(structure: dict[Any, Any] | list[dict[Any, Any]]) -> str:
    messages_json = json.dumps(structure, indent=3, ensure_ascii=False, default=str)
    messages_formatted = f"<pre>{messages_json}</pre>"

    return messages_formatted


async def SendTemporaryFileFromText(chat_id: int, text: str) -> None:
    file_path = DIR_TEMP / f"chat_id_{chat_id}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

    await SendDocument(chat_id=chat_id, document=types.FSInputFile(file_path))

    os.remove(file_path)


async def DownloadImage(photo: types.PhotoSize) -> None:
    file = await bot.get_file(photo.file_id)
    assert file.file_path is not None, "File path is None"

    await bot.download_file(
        file.file_path,
        destination=DIR_IMAGES / f"{file.file_id}.png",
    )


# reupload images and restore their file_ids
async def AccessImage(file_id: str) -> types.FSInputFile:
    return types.FSInputFile(DIR_IMAGES / f"{file_id}.png")
