from pydantic import UUID4
from sqlmodel import SQLModel, Field

from src.domain.entities.template_entity import TemplateEntity


class Template(SQLModel, TemplateEntity, table=True):
	id: UUID4 = Field(primary_key=True)
