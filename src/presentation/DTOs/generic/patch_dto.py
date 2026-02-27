from typing import Literal

from pydantic import BaseModel, Field

"""aaa"""


class PatchDTO(BaseModel):
	"""Represents a patch object"""

	op: Literal["add", "remove", "test", "replace"] = Field(
		title="op", description="Operation type (one between 'add', 'remove', 'test', 'replace')."
	)

	path: str = Field(title="path", description="Path of the field on which operation is applied.")

	value: object = Field(title="value", description="Value to be assigned to the field.")
