from neomodel import config

from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton


class GraphDatabaseManager(metaclass=Singleton):
	"""
	Utility class to manage connection to Graph database connection.
	"""

	def __init__(self):
		"""
		Initialize the connection to Graph database.
		"""

		config.DATABASE_URL = f"bolt://{SETTINGS.GRAPH_DB_USER}:{SETTINGS.GRAPH_DB_PASSWORD.get_secret_value()}@{SETTINGS.GRAPH_DB_HOST}:{SETTINGS.GRAPH_DB_PORT}"
