from src.domain.errors.error import Error


class GenericErrors:
	"""Generic errors container"""

	@staticmethod
	def generic_error(details: str) -> Error:
		"""
		Creates a new generic error with details passed as parameter and 500 as status code.

		:param str details: error details.
		:return: an Error object with the given details.
		:rtype: Error
		"""

		return Error(
			message=f"A generic error occurred. Details: {details}",
			status_code=500,
		)

	@staticmethod
	def not_found_error(key: str, type: str | None = None) -> Error:
		"""
		Creates a NotFound error with the given details and 404 as status code.

		:param str key: not found key.
		:param str | None type: type of object searched. Default to None.
		:return: an Error object with the given details.
		:rtype: Error
		"""

		return Error(
			message=f"Entry of type {type} with key={key} does not exist."
			if type
			else f"Entry with key={key} does not exist.",
			status_code=404,
		)
