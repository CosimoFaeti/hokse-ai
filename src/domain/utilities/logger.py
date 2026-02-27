import logging

from src.domain.utilities.constants import LOG_DATE_FORMAT
from src.domain.utilities.settings import SETTINGS

# Inspired by https://medium.com/@emanueleorecchio/crafting-your-custom-logger-in-python-a-step-by-step-guide-0824bfd9b939


class CustomFormatter(logging.Formatter):
	"""
	Custom formatter.
	"""

	grey = "\x1b[37;1m"
	yellow = "\x1b[33;20m"
	red = "\x1b[31;20m"
	bold_red = "\x1b[31;1m"
	green = "\x1b[1;32m"
	reset = "\x1b[0m"
	format: str = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
	# TODO datefmt should be here

	FORMATS = {
		logging.DEBUG: grey + format + reset,
		logging.INFO: green + format + reset,
		logging.WARNING: yellow + format + reset,
		logging.ERROR: red + format + reset,
		logging.CRITICAL: bold_red + format + reset,
	}

	def format(self, record: logging.LogRecord) -> str:
		"""
		Format a log line.

		:param loggingRecord record: log record to be formatted.
		:return: formatted log record
		:rtype: str
		"""

		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(fmt=log_fmt, datefmt=LOG_DATE_FORMAT)
		return formatter.format(record=record)


class Logger(logging.Logger):
	"""Logger class."""

	def __init__(self, name: str, level: int | str = logging.NOTSET):
		"""
		Initializes the logger with the already defined CustomFormatter.

		:param str name: logger name.
		:param int | str level: logger level.
		"""

		super().__init__(name, level)
		self.extra_info = None

		handler = logging.StreamHandler()
		handler.setFormatter(fmt=CustomFormatter())
		self.addHandler(hdlr=handler)


match SETTINGS.LOG_LEVEL:
	case "debug":
		log_level = logging.DEBUG
	case "info":
		log_level = logging.INFO
	case "warning":
		log_level = logging.WARNING
	case "error":
		log_level = logging.ERROR
	case _:
		log_level = logging.INFO

logger = Logger(name="python-api-template", level=log_level)
