from pathlib import Path

_DIR_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
_DIR_DATA = _DIR_ROOT / "data"
_DIR_LOGS = _DIR_DATA / "logs"

DIR_TEMP = _DIR_DATA / "temp"

_dirs = [
    _DIR_DATA,
    _DIR_LOGS,
    DIR_TEMP,
]

PATH_ENV = _DIR_ROOT / ".env"
PATH_BOT_LOGS = _DIR_LOGS / "bot" / "bot.log"

PATH_TERMS_OF_USE = _DIR_ROOT / "docs" / "papers" / "terms_of_service.pdf"


def EnsurePaths() -> None:
    for directory in _dirs:
        directory.mkdir(parents=True, exist_ok=True)

    if not PATH_ENV.exists():
        raise FileNotFoundError("`.env` file not found")
