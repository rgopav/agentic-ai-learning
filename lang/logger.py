import logging
from datetime import datetime
from pathlib import Path

# All scripts share a single logs/ folder at the workspace root
_LOGS_DIR = Path(__file__).parent.parent / "logs"


def get_logger(script_name: str) -> logging.Logger:
    """
    Returns a named logger that writes to a daily rotating log file.

    Log location : <workspace>/logs/YYYY-MM-DD.log
    Console      : INFO and above
    File         : DEBUG and above (full detail)

    Usage:
        from logger import get_logger
        log = get_logger(__name__)   # or pass any descriptive name
        log.info("Step started")
        log.debug("Variable value: %s", value)
    """
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = _LOGS_DIR / f"{today}.log"

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)

    # Guard against duplicate handlers if this module is imported multiple times
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(name)-35s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — captures everything (DEBUG+) for post-mortem analysis
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    # Console handler — shows INFO+ so the terminal stays readable
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
