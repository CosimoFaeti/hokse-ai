from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.logger import logger


# Inspired from https://medium.com/swlh/handling-exceptions-in-python-a-cleaner-way-using-decorators-fae22aa0abec


def exception_handler(func):
	"""
	Decorator for managing function failures.

	:param func:
	:return:
	"""

	def inner_function(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			logger.error(msg=f"An generic error occurred in {func.__name__}. Details: {str(e)}")
			return Result.fail(error=GenericErrors.generic_error(details=str(e)))

	return inner_function
