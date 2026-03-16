# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import logging
import os
import sys

_FMT_DEFAULT = '%(asctime)s | [%(levelname)s] %(message)s'
_FMT_DEBUG = '%(asctime)s | [%(levelname)s] %(filename)s:%(lineno)d:%(funcName)s:%(message)s'


class _NmsLogger(logging.Logger):
    """Package logger with level-aware formatting and exception handling."""

    class _Formatter(logging.Formatter):
        """Use debug format (filename/line/func) for all records when root logger is at DEBUG level."""

        def format(self, record: logging.LogRecord) -> str:
            self._style._fmt = (
                _FMT_DEBUG if logging.getLogger().isEnabledFor(logging.DEBUG) else _FMT_DEFAULT
            )
            return super().format(record)

    @staticmethod
    def _ensure_formatter() -> None:
        for handler in logging.getLogger().handlers:
            if not isinstance(handler.formatter, _NmsLogger._Formatter):
                handler.setFormatter(_NmsLogger._Formatter())

    def _log(self, level, msg, args, exc_info=None, **kwargs):
        if exc_info and not self.isEnabledFor(logging.DEBUG):
            exc_info = None
        _NmsLogger._ensure_formatter()
        kwargs['stacklevel'] = kwargs.get('stacklevel', 1) + 1
        super()._log(level, msg, args, exc_info=exc_info, **kwargs)


def get_logger(name: str) -> _NmsLogger:
    """Return an _NmsLogger for the given name.

    Log level is controlled via the LOG_LEVEL environment variable
    (e.g. DEBUG, INFO, WARNING, ERROR). Defaults to INFO.
    """
    if not logging.getLogger().handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_NmsLogger._Formatter())
        logging.getLogger().addHandler(handler)

    #  1. Save the current logger class (likely the default logging.Logger)
    #  2. Temporarily set _NmsLogger as the logger class — so the next getLogger call creates an _NmsLogger instance
    #     if one doesn't exist yet for that name
    #  3. Get (or create) the logger for name
    #  4. Restore the original logger class immediately after to not affect other loggers with this custom formatting
    old_class = logging.getLoggerClass()
    logging.setLoggerClass(_NmsLogger)
    logger = logging.getLogger(name)
    logging.setLoggerClass(old_class)

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, level, logging.INFO)
    logger.setLevel(numeric_level)
    logging.getLogger().setLevel(numeric_level)

    return logger  # type: ignore[return-value]
