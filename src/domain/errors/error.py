class Error:
	"""Represents a generic error.

	:param str message: a message that describes the error.
	:param int status_code: an HTTP status code that can be associated to the error. Defaults to 500.
	"""

	def __init__(self, message: str, status_code: int = 500):
		"""
		Initialize a new error.

		:param str message: error message
		:param int status_code: error status code. Default to 500.
		"""

		self.message = message
		self.status_code = status_code
