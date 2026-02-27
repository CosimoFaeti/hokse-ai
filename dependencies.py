from src.application.services.graph_template_service import GraphTemplateService
from src.application.services.nosql_template_service import NoSQLTemplateService
from src.application.services.sql_template_service import SQLTemplateService
from src.application.services.vector_template_service import VectorTemplateService


def get_sql_template_service() -> SQLTemplateService:
    raise NotImplementedError()

def get_nosql_template_service() -> NoSQLTemplateService:
    raise NotImplementedError()

def get_graph_template_service() -> GraphTemplateService:
    raise NotImplementedError()

def get_vector_template_service() -> VectorTemplateService:
    raise NotImplementedError()