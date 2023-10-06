import logging

from ecs_logging import StdlibFormatter

from settings import app_settings

log_handler = logging.StreamHandler()

if app_settings.ENABLE_LOG_FORMATTER:
    log_handler.setFormatter(StdlibFormatter())

__all__ = ["log_handler"]
