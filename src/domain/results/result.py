from typing import TypeVar, Generic

from src.domain.errors.error import Error

T = TypeVar("T")


class Result(Generic[T]):
	"""
	Represents the outcome of an operation.

	:param object | None value: the value returned by the operation, if successful. Defaults to None.
	:param Error | None error: the error returned by the operation, if not successful. Defaults to None.
	"""

	def __init__(self, value: T | None = None, error: Error | None = None):
		"""
		Initialize a new Result object.

		:param object | None value: the value returned by the operation, if successful. Defaults to None.
		:param Error | None error: the error returned by the operation, if not successful. Defaults to None.
		"""

		self.value: T = value
		self.error = error

	@property
	def failed(self) -> bool:
		"""
		Utility function used to check if a Result contains a not successful outcome.

		:return: True if the operation has failed, False otherwise.
		:rtype: bool
		"""

		return self.error is not None

	@property
	def success(self) -> bool:
		"""
		Utility function used to check if a Result contains a successful outcome.

		:return: True if the operation has been successful, False otherwise.
		:rtype: bool
		"""

		return self.error is None

	@classmethod
	def fail(cls, error: Error):
		"""
		Create a Result object for a failed operation.

		:param Error error: error used to initialize the Result object.
		:return: a Result object with the given error.
		:rtype: Result
		"""
		return cls(value=None, error=error)

	@classmethod
	def ok(cls, value: T = None):
		"""
		Create a Result object for a successful operation.

		:param T value: outcome of the operation. Default to None.
		:return: a Result object with the given value.
		:rtype: Result
		"""
		return cls(value=value, error=None)
