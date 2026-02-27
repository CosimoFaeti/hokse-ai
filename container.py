# app/core/container.py
from dependency_injector import containers, providers

from src.application.services.nosql_template_service import NoSQLTemplateService
from src.application.services.sql_template_service import SQLTemplateService
from src.infrastructure.clients.langchain_client import LangchainClient
from src.infrastructure.clients.redis_client import RedisClient
from src.persistence.repositories.nosql_template_repository import NoSQLTemplateRepository
from src.persistence.repositories.sql_template_repository import SQLTemplateRepository
from src.persistence.repositories.vector_template_repository import VectorTemplateRepository


class Container(containers.DeclarativeContainer):
	# Infrastructure layer implementations (these might still be instances)
	langchain_client = providers.Singleton(LangchainClient)
	redis_client = providers.Singleton(RedisClient)

	# Repository implementations (just class references since methods are static)
	sql_template_repository = providers.Factory(lambda: SQLTemplateRepository)
	nosql_template_repository = providers.Factory(lambda: NoSQLTemplateRepository)
	vector_template_repository = providers.Factory(lambda: VectorTemplateRepository)
	graph_template_repository = providers.Factory(lambda: NoSQLTemplateRepository)

	# Application services
	sql_template_service = providers.Singleton(
		SQLTemplateService,
		repository=sql_template_repository
	)

	nosql_template_service = providers.Singleton(
		NoSQLTemplateService,
		repository=nosql_template_repository,
	)

	vector_template_service = providers.Singleton(
		NoSQLTemplateService,
		repository=vector_template_repository,
		langchain_client=langchain_client
	)

	graph_template_service = providers.Singleton(
		NoSQLTemplateService,
		repository=graph_template_repository,
	)