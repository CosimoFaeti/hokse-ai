from fastapi import APIRouter, HTTPException, Body, Path, Depends
from pydantic import UUID4

from dependencies import get_nosql_template_service
from src.application.services.nosql_template_service import NoSQLTemplateService
from src.domain.entities.patch_entity import PatchEntity
from src.domain.entities.template_entity import TemplateEntity
from src.domain.results.result import Result
from src.domain.utilities.logger import logger
from src.presentation.DTOs.generic.patch_dto import PatchDTO
from src.presentation.DTOs.templates.nosql.delete_templates_output_dto import DeleteTemplateOutputDTO
from src.presentation.DTOs.templates.nosql.get_templates_output_dto import GetTemplateOutputDTO
from src.presentation.DTOs.templates.nosql.patch_templates_output_dto import PatchTemplateOutputDTO
from src.presentation.DTOs.templates.nosql.post_templates_input_dto import PostTemplateInputDTO
from src.presentation.DTOs.templates.nosql.post_templates_output_dto import PostTemplateOutputDTO
from src.presentation.DTOs.templates.nosql.put_templates_input_dto import PutTemplateInputDTO
from src.presentation.DTOs.templates.nosql.put_templates_output_dto import PutTemplateOutputDTO
from src.presentation.examples.templates.nosql.delete_templates_request_examples import DELETE_TEMPLATES_PATH_EXAMPLE
from src.presentation.examples.templates.nosql.delete_templates_response_examples import (
	DELETE_TEMPLATES_RESPONSE_EXAMPLES,
)
from src.presentation.examples.templates.nosql.get_templates_request_examples import GET_TEMPLATES_PATH_EXAMPLE
from src.presentation.examples.templates.nosql.get_templates_response_examples import GET_TEMPLATES_RESPONSE_EXAMPLES
from src.presentation.examples.templates.nosql.patch_templates_request_examples import (
	PATCH_TEMPLATES_PATH_EXAMPLE,
	PATCH_TEMPLATES_BODY_EXAMPLES,
)
from src.presentation.examples.templates.nosql.patch_templates_response_examples import (
	PATCH_TEMPLATES_RESPONSE_EXAMPLES,
)
from src.presentation.examples.templates.nosql.post_templates_request_examples import POST_TEMPLATES_BODY_EXAMPLES
from src.presentation.examples.templates.nosql.post_templates_response_examples import POST_TEMPLATES_RESPONSE_EXAMPLES
from src.presentation.examples.templates.nosql.put_templates_request_examples import (
	PUT_TEMPLATES_PATH_EXAMPLE,
	PUT_TEMPLATES_BODY_EXAMPLES,
)
from src.presentation.examples.templates.nosql.put_templates_response_examples import PUT_TEMPLATES_RESPONSE_EXAMPLES
from src.presentation.mappers.generic.patch_mappers import PatchMappers

from src.presentation.mappers.templates.nosql.delete_templates_mappers import DeleteTemplateMappers
from src.presentation.mappers.templates.nosql.get_templates_mappers import GetTemplateMappers
from src.presentation.mappers.templates.nosql.patch_templates_mappers import PatchTemplateMappers
from src.presentation.mappers.templates.nosql.post_template_mappers import PostTemplateMappers
from src.presentation.mappers.templates.nosql.put_templates_mappers import PutTemplateMappers

nosql_template_router = APIRouter(prefix="/nosql/templates", tags=["NoSQL"])


# region POST
@nosql_template_router.post(
	path="/",
	summary="Create a new template.",
	description="Create a new template.",
	status_code=201,
	responses=POST_TEMPLATES_RESPONSE_EXAMPLES,
)
async def create_template(
	dto: PostTemplateInputDTO = Body(examples=POST_TEMPLATES_BODY_EXAMPLES),
	nosql_template_service: NoSQLTemplateService = Depends(get_nosql_template_service)
) -> PostTemplateOutputDTO:
	"""
	Create a new ``template``.

	:param PostTemplateInputDTO dto: an object containing the information used to initialize the ``template``
	:return: the created ``template``
	:rtype: PostTemplateOutputDTO
	:raises: HTTPException
	"""

	logger.info(msg="Calling POST /nosql/templates")

	entity: TemplateEntity = PostTemplateMappers.to_entity(dto=dto)

	result: Result[TemplateEntity] = await nosql_template_service.post(entity=entity)

	if result.failed:
		raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

	output: PostTemplateOutputDTO = PostTemplateMappers.to_dto(entity=result.value)

	logger.info(msg="Successfully returning from POST /nosql/templates")

	return output


# endregion


# region GET
@nosql_template_router.get(
	path="/{id}",
	summary="Get a template.",
	description="Retrieve a template from its id.",
	responses=GET_TEMPLATES_RESPONSE_EXAMPLES,
)
async def get_template(
	id: UUID4 = Path(example=GET_TEMPLATES_PATH_EXAMPLE),
	nosql_template_service: NoSQLTemplateService = Depends(get_nosql_template_service)

) -> GetTemplateOutputDTO:
	"""
	Get the ``template`` with the given id.

	:param UUID4 id: id of the ``template`` to be retrieved.
	:return: the ``template`` with the given id, if it exists
	:rtype: GetTemplateOutputDTO
	:raises: HTTPException
	"""

	logger.info(msg="Calling GET /nosql/templates")

	result: Result[TemplateEntity] = await nosql_template_service.get(id=id)

	if result.failed:
		raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

	output: GetTemplateOutputDTO = GetTemplateMappers.to_dto(entity=result.value)

	logger.info(msg="Successfully returning from GET /nosql/templates")

	return output


# endregion


# region DELETE
@nosql_template_router.delete(
	path="/{id}",
	summary="Delete a template.",
	description="Delete a template with the given id.",
	responses=DELETE_TEMPLATES_RESPONSE_EXAMPLES,
)
async def delete_template(
	id: UUID4 = Path(example=DELETE_TEMPLATES_PATH_EXAMPLE),
	nosql_template_service: NoSQLTemplateService = Depends(get_nosql_template_service)
) -> DeleteTemplateOutputDTO:
	"""
	Delete the ``template`` with the given id.

	:param UUID4 id: id of the ``template`` to delete.
	:return: the deleted ``template`` if it exists.
	:rtype: DeleteTemplateOutputDTO
	:raises: HTTPException
	"""

	logger.info(msg="Calling DELETE /nosql/templates")

	result: Result[TemplateEntity] = await nosql_template_service.delete(id=id)

	if result.failed:
		raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

	output: DeleteTemplateOutputDTO = DeleteTemplateMappers.to_dto(entity=result.value)

	logger.info(msg="Successfully returning from DELETE /nosql/templates")

	return output


# endregion


# region PUT
@nosql_template_router.put(
	path="/{id}",
	summary="Update a template.",
	description="Update the template with the given id.",
	responses=PUT_TEMPLATES_RESPONSE_EXAMPLES,
)
async def put_template(
	id: UUID4 = Path(example=PUT_TEMPLATES_PATH_EXAMPLE),
	dto: PutTemplateInputDTO = Body(examples=PUT_TEMPLATES_BODY_EXAMPLES),
	nosql_template_service: NoSQLTemplateService = Depends(get_nosql_template_service)
) -> PutTemplateOutputDTO:
	"""
	Replace the ``template`` with the given id with the one passed as parameter.

	:param UUID4 id: id of the ``template`` to be replaced.
	:param PutTemplateInputDTO dto: the ``template`` used to replace the old one.
	:return: the updated ``template``
	:rtype: PutTemplateOutputDTO
	:raises: HTTPException
	"""

	logger.info(msg="Calling PUT /nosql/templates")

	entity: TemplateEntity = PutTemplateMappers.to_entity(dto=dto)

	result: Result[TemplateEntity] = await nosql_template_service.put(id=id, entity=entity)

	if result.failed:
		raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

	output: PutTemplateOutputDTO = PutTemplateMappers.to_dto(entity=result.value)

	logger.info(msg="Successfully returning from PUT /nosql/templates")

	return output


# endregion


# region PATCH
@nosql_template_router.patch(
	path="/{id}",
	summary="Patch a template.",
	description="Patch the template with the given id.",
	responses=PATCH_TEMPLATES_RESPONSE_EXAMPLES,
)
async def patch_template(
	id: UUID4 = Path(example=PATCH_TEMPLATES_PATH_EXAMPLE),
	dto: list[PatchDTO] = Body(examples=PATCH_TEMPLATES_BODY_EXAMPLES),
	nosql_template_service: NoSQLTemplateService = Depends(get_nosql_template_service)
) -> PatchTemplateOutputDTO:
	"""
	Apply the patches passed as parameter to the ``template`` with the given id.

	:param UUID4 id: id of the ``template`` to patch.
	:param list[PatchDTO] dto: list of patches to be applied.
	:return: the patched ``template``
	:rtype: PatchTemplateOutputDTO
	:raises: HTTPException
	"""

	logger.info(msg="Calling PATCH /nosql/templates")

	entities: list[PatchEntity] = [PatchMappers.to_entity(dto=patch) for patch in dto]

	result: Result[TemplateEntity] = await nosql_template_service.patch(id=id, patches=entities)

	if result.failed:
		raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

	output: PatchTemplateOutputDTO = PatchTemplateMappers.to_dto(entity=result.value)

	logger.info(msg="Successfully returning from PATCH /nosql/templates")

	return output


# endregion
