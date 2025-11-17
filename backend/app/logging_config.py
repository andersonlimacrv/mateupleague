import logging
import sys
from loguru import logger


class InterceptHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        logger.remove()
        logger.add(
            sys.stderr,
            level="INFO",
            colorize=True,
            format="<green>INFO:</green>     [<cyan>{time:HH:mm:ss}</cyan>] <level>- {message}</level>",
        )

    def emit(self, record):
        if not record.name.startswith("sqlalchemy.engine"):
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelname, record.getMessage())
