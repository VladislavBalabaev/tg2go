import logging
from pathlib import Path

from aiogram import types

from tg2go.bot.lifecycle.creator import bot
from tg2go.core.configs.paths import DIR_CLIENT_HEADER, DIR_IMAGES, DIR_STAFF_HEADER
from tg2go.db.models.common.types import GoodId


def GetGoodImageDir(good_id: GoodId) -> Path:
    directory = DIR_IMAGES / str(good_id)
    directory.mkdir(parents=True, exist_ok=True)

    return directory


def GetClientHeaderDir() -> Path:
    return DIR_CLIENT_HEADER


def GetStaffHeaderDir() -> Path:
    return DIR_STAFF_HEADER


class Image:
    def __init__(self, path: Path):
        self.source: Path = path / "source.png"
        self.file_id: Path = path / "file_id.txt"

    def GetFileId(self) -> str:
        self.file_id.touch(exist_ok=True)

        return Path(self.file_id).read_text(encoding="utf-8").strip()

    def GetSource(self) -> types.FSInputFile:
        if not self.source.exists():
            raise ValueError(f"Image source file {self.source} doesn't exists.")

        return types.FSInputFile(self.source)

    def UpdateFileId(self, file_id: str) -> None:
        logging.info(f"Updating file_id={file_id} at {self.file_id}.")

        self.file_id.write_text(file_id, encoding="utf-8")

    async def DownloadSource(self, photo: types.PhotoSize) -> None:
        file = await bot.get_file(photo.file_id)
        assert file.file_path is not None, "File path is None"

        await bot.download_file(file.file_path, destination=self.source)
        self.UpdateFileId(photo.file_id)

        logging.info(f"Photo file_id={photo.file_id} is downloaded to {self.source}.")
