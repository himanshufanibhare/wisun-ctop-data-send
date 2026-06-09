import logging
from pathlib import Path
from typing import Optional


LOG_DIRECTORY = "logs"
LOG_FILE_NAME = "coap_rest_bridge.log"
CONSOLE_LOG_LEVEL = "INFO"
FILE_LOG_LEVEL = "DEBUG"


def setup_logging(
    log_dir: Optional[str] = None,
) -> logging.Logger:
    project_root = Path(__file__).resolve().parent
    resolved_log_dir = (
        project_root / LOG_DIRECTORY if log_dir is None else Path(log_dir)
    )

    Path(resolved_log_dir).mkdir(parents=True, exist_ok=True)

    console_level = getattr(logging, CONSOLE_LOG_LEVEL.upper(), logging.INFO)
    file_level = getattr(logging, FILE_LOG_LEVEL.upper(), logging.DEBUG)
    log_file_path = resolved_log_dir / LOG_FILE_NAME

    logger = logging.getLogger("coap_rest_bridge")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
