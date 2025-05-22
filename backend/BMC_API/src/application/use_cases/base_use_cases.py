# application/use_cases/base_use_cases.py
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

from loguru import logger
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.exc import NoResultFound

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.core.exceptions import NotFoundException, RepositoryException
from BMC_API.src.domain.repositories.base_repository import BaseRepositoryProtocol
from BMC_API.src.infrastructure.persistence.base import Base

# Generic type for entities that inherit from Base
T = TypeVar("T", bound=Base)
# Generic type for DTOs
ResponseDTO = TypeVar("ResponseDTO")
CreateDTO = TypeVar("CreateDTO", bound=BaseModel)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseModel)


class BaseService(Generic[T, ResponseDTO]):
    """
    Base service providing generic CRUD operations that can be inherited
    by specific service implementations.
    """

    def __init__(self, repository: BaseRepositoryProtocol, dto_class=None):
        """
        Initialize the base service with a repository and optional DTO class.

        Args:
            repository: The repository for database operations
            dto_class: The DTO class used to transform entities to response objects
        """
        self.repository = repository
        self.dto_class = dto_class
        self.model_name = str(self.repository.model.__name__).replace("Model", "")

    async def get_raw(self, id: int) -> Optional[Base]:
        """
        Get an entity by id and return raw database model.

        Args:
            id: The entity id

        Returns:
            The entity as raw database model if found

        Raises:
            ValueError: If no id is provided
            NotFoundException: If the entity is not found
        """
        if id is None:
            raise ValueError("id must be provided.")

        entity = await self.repository.get(id=id)
        if not entity:
            raise NotFoundException(message=f"{self.model_name} with id {id} not found.")
        return entity

    async def get(self, id: int) -> Optional[ResponseDTO]:
        """
        Get an entity by id and convert it to a DTO if found.

        Args:
            id: The entity id

        Returns:
            The entity as a DTO if found

        Raises:
            ValueError: If no id is provided
            NotFoundException: If the entity is not found
        """
        try:
            entity = await self.get_raw(id=id)
        except NotFoundException as e:
            logger.error(f"Error getting entity: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error getting entity: {e}")
            raise RepositoryException(message=f"Error getting entity: {str(e)}")

        # If dto_class is provided, use it to convert the entity
        if self.dto_class:
            return self.dto_class.model_validate(entity)
        return entity

    async def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        search_filters: Dict[str, Any] | None = None,
        output_filters: List[str] | None = None,
        sort_by: str | None = "id",
        sort_desc: bool | None = False,
    ) -> Tuple[Optional[List[ResponseDTO]], int, int]:
        """
        List entities with pagination, filtering and sorting options.

        Args:
            limit: Maximum number of entities to return
            offset: Number of entities to skip
            search_filters: Dictionary of field:value pairs to filter entities
            output_filters: List of fields to include in the response
            sort_by: Field to sort by
            sort_desc: Whether to sort in descending order

        Returns:
            Tuple of (entities as DTOs, total pages, total records)

        Raises:
            NotFoundException: If no entities are found
        """
        try:
            entities, total_pages, total_records = await self.repository.list(
                limit=limit,
                offset=offset,
                search_filters=search_filters,
                output_filters=output_filters,
                sort_by=sort_by,
                sort_desc=sort_desc,
            )
        except Exception as e:
            logger.error(f"Error listing entity: {e}")
            raise RepositoryException(message=f"Error listing entity: {str(e)}")

        if not entities:
            raise NotFoundException(message=f"No {self.model_name} found.")

        # Convert entities to DTOs if dto_class is provided
        if self.dto_class:
            return (
                TypeAdapter(List[self.dto_class]).validate_python(entities),
                total_pages,
                total_records,
            )
        return entities, total_pages, total_records

    async def create(self, model_create: Dict) -> ResponseDTO:
        """
        Create a new entity from a DTO.

        Args:
            model_create: The DTO containing the data for the new entity

        Returns:
            The created entity as a DTO

        Raises:
            RepositoryException: If there's an error creating the entity or validating the response
        """
        try:
            # Convert dict to self.repository.model with model_create data
            new_entity = self.repository.model(**model_create)
            created = await self.repository.create_obj(new_entity)

            # Convert created entity to response DTO
            if self.dto_class:
                return self.dto_class.model_validate(created)
            return created

        except Exception as e:
            logger.error(f"Error creating entity: {e}")
            raise RepositoryException(message=f"Error creating entity: {str(e)}")

    async def update(self, id: int, model_update: Dict) -> ResponseDTO:
        """
        Update an entity by id with data from a DTO.

        Args:
            id: The id of the entity to update
            model_update: The DTO containing the updated data

        Returns:
            The updated entity as a DTO

        Raises:
            ValueError: If no id is provided
            NotFoundException: If the entity is not found
            RepositoryException: If there's an error updating the entity
        """
        if id is None:
            raise ValueError("id must be provided for update.")

        # Check if entity exists
        existing = await self.repository.get(id=id)
        if not existing:
            raise NotFoundException(message=f"{self.model_name} with id {id} not found for update.")

        try:
            # Update the entity
            updated = await self.repository.update(id, model_update)

            # Convert updated entity to response DTO
            if self.dto_class:
                return self.dto_class.model_validate(updated)
            return updated

        except Exception as e:
            logger.error(f"Error updating {self.model_name} with {id}: {e}")
            raise RepositoryException(message=f"Error updating {self.model_name} with id {id}: {str(e)}")

    async def update_bulk(
        self, updates: List[Dict[str, Any]], update_dto_class=None
    ) -> BulkOperationResponse[ResponseDTO]:
        """
        Perform bulk updates and return both successful and failed results.

        Returns a dictionary containing:
        - 'successful': List of successfully updated entities
        - 'failed': List of failed updates with error details
        """
        successful_results = []
        failed_results = []
        # dto_class = update_dto_class or UpdateDTO

        for update_data in updates:
            if "id" not in update_data:
                failed_results.append({"data": update_data, "error": f"Missing {self.model_name} id"})
                logger.warning(f"Skipping update for {self.model_name} without id")
                continue

            entity_id = update_data.pop("id")
            original_data = {"id": entity_id, **update_data}

            try:
                # Get the existing entity to confirm it exists
                existing = await self.repository.get(id=entity_id)
                if not existing:
                    failed_results.append({
                        "data": original_data,
                        "error": f"{self.model_name} with id {entity_id} not found",
                    })
                    logger.warning(f"{self.model_name} with id {entity_id} not found for update")
                    continue

                # # Convert dict to the specified UpdateDTO for validation
                # model_update = dto_class(**update_data)

                # Update the entity
                updated = await self.repository.update(entity_id, update_data)

                # Convert updated entity to response DTO
                if self.dto_class:
                    successful_results.append(self.dto_class.model_validate(updated))
                else:
                    successful_results.append(updated)

            except Exception as e:
                failed_results.append({"data": original_data, "error": str(e)})
                logger.error(f"Error updating {self.model_name} with id {entity_id}: {e}")
                continue

        return BulkOperationResponse[Any](
            detail=f"Bulk update completed: {len(successful_results)} successful, {len(failed_results)} failed.",
            successful=successful_results,
            failed=failed_results,
        )

    async def delete(self, id: int) -> Dict:
        """
        Delete an entity by id.

        Args:
            id: The entity id

        Returns:
            The result of the delete operation

        Raises:
            ValueError: If no id is provided
            NotFoundException: If the entity is not found
        """
        if id is None:
            raise ValueError("id must be provided for deletion.")

        try:
            await self.repository.delete(id=id)
        except NoResultFound as e:
            logger.error(f"Error deleting {self.model_name} with id {id}: {e}")
            raise NotFoundException(message=f"{self.model_name} with id {id} not found for delete.")
        except Exception as e:
            logger.error(f"Error deleting entity with id {id}: {e}")
            raise RepositoryException(message=f"Error updating {self.model_name} with id {id}: {str(e)}")

    async def delete_bulk(self, ids: List[int]) -> BulkOperationResponse[Any]:
        """
        Delete multiple entities by their IDs.

        Args:
            ids: List of entity IDs to delete

        Returns:
            List of successful deletion results
        """
        successful_results = []
        failed_results = []

        for entity_id in ids:
            try:
                await self.repository.delete(id=entity_id)
                successful_results.append(entity_id)
            except NoResultFound:
                failed_results.append({
                    "id": entity_id,
                    "error": f"{self.model_name} with id {entity_id} not found.",
                })
                logger.warning(f"{self.model_name} with id {entity_id} not found for deletion.")
            except Exception as e:
                failed_results.append({"id": entity_id, "error": str(e)})
                logger.error(f"Error deleting {self.model_name} with id {entity_id}: {e}")
                continue

        return BulkOperationResponse[Any](
            detail=f"Bulk delete completed: {len(successful_results)} successful, {len(failed_results)} failed.",
            successful=successful_results,
            failed=failed_results,
        )

    async def check_ownership(self, user_id: int, model_id: int, model_id_field: str) -> bool:
        """
        Check whether the entity with model_id belongs to the given user_id.

        Args:
            user_id: The ID of the user to check ownership for.
            model_id: The ID of the model entity.
            model_id_field: The attribute name on the model that holds the owner/user ID.

        Returns:
            True if user_id owns the model instance, False otherwise.

        Raises:
            NotFoundException: If the entity is not found.
            AttributeError: If the specified ownership field doesn't exist on the entity.
        """
        entity = await self.repository.get(id=model_id)
        if not entity:
            raise NotFoundException(message="You don't have permission to access this resource.")
            # raise NotFoundException(message=f"{self.model_name} with id {model_id} not found for ownership check.")

        try:
            owner_id = getattr(entity, model_id_field)
        except AttributeError:
            raise AttributeError(f"{self.model_name} does not have a field named '{model_id_field}'.")

        return owner_id == user_id
