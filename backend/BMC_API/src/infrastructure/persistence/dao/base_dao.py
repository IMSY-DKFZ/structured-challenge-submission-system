# BMC_API/src/infrastructure/persistence/base_dao.py
import math
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.infrastructure.persistence.base import Base

DataObject = TypeVar("DataObject", bound=Base)


class QueryHelper(Generic[DataObject]):
    """Helper class for query building operations."""

    def __init__(self, model_class: Type[DataObject]):
        self.model = model_class

    def build_query_with_output_filters(self, output_filters: List[str] | None = None):
        """Build the initial query with output filters if specified."""
        if output_filters:
            selected_columns = [getattr(self.model, field) for field in output_filters if hasattr(self.model, field)]
            if not selected_columns:  # Fallback if no valid columns provided
                return select(self.model)
            else:
                return select(*selected_columns)
        else:
            return select(self.model)

    def apply_search_filters(self, query, search_filters: Dict[str, Any] | None = None):
        """Apply search filters to query and return both the filtered query and a base query for counting."""
        base_query = select(self.model)

        if not search_filters:
            return query, base_query

        for field, value in search_filters.items():
            # Handle NULL values
            if value is None:
                condition = self._build_null_condition(field)
                if condition is not None:
                    query = query.filter(condition)
                    base_query = base_query.filter(condition)
                continue

            # Handle operators
            if "__" in field:
                condition = self._build_operator_condition(field, value)
                if condition is not None:
                    query = query.filter(condition)
                    base_query = base_query.filter(condition)
            else:
                # Simple equality
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    query = query.filter(column == value)
                    base_query = base_query.filter(column == value)
                else:
                    logger.exception(f"Field {field} not found in model {self.model.__name__}")
                    raise NoResultFound(f"Field {field} not found in model {self.model.__name__}")

        return query, base_query

    def _build_null_condition(self, field: str):
        """Build condition for NULL value checks."""
        if field.endswith("__notnull"):
            field_name = field.rsplit("__", 1)[0]
            if hasattr(self.model, field_name):
                return getattr(self.model, field_name).isnot(None)
        elif field.endswith("__isnull"):
            field_name = field.rsplit("__", 1)[0]
            if hasattr(self.model, field_name):
                return getattr(self.model, field_name).is_(None)
        else:
            # Direct NULL comparison
            if hasattr(self.model, field):
                return getattr(self.model, field).is_(None)

        logger.warning(f"Field {field} not found in model {self.model.__name__}")
        return None

    def _build_operator_condition(self, field: str, value: Any):
        """Build condition based on field operator suffix."""
        field_name, op = field.rsplit("__", 1)

        if not hasattr(self.model, field_name):
            logger.warning(f"Field {field_name} not found in model {self.model.__name__}")
            return None

        column = getattr(self.model, field_name)

        # Map of operators to their implementations
        operator_map = {
            "lt": lambda col, val: col < val,
            "lte": lambda col, val: col <= val,
            "le": lambda col, val: col <= val,
            "gt": lambda col, val: col > val,
            "gte": lambda col, val: col >= val,
            "ge": lambda col, val: col >= val,
            "ne": lambda col, val: col != val,
            "like": lambda col, val: col.like(f"%{val}%"),
            "ilike": lambda col, val: col.ilike(f"%{val}%"),
            "startswith": lambda col, val: col.like(f"{val}%"),
            "endswith": lambda col, val: col.like(f"%{val}"),
            # "contains": lambda col, val: col.like(f"%{val}%"),
            "contains":  lambda col, val: col.contains(val),
        }

        # Handle special cases
        if op == "between" and isinstance(value, (list, tuple)) and len(value) == 2:
            return column.between(value[0], value[1])
        elif op == "in" and isinstance(value, (list, tuple)):
            return column.in_(value)
        elif op in operator_map:
            return operator_map[op](column, value)
        else:
            logger.warning(f"Unsupported operator: {op}")
            return None

    def apply_sorting(self, query, sort_by: str | None = None, sort_desc: bool = False):
        """Apply sorting to the query."""
        if not sort_by:
            return query

        sort_fields = [x.strip() for x in sort_by.split(",")] if isinstance(sort_by, str) else [sort_by]

        for field in sort_fields:
            is_desc = field.startswith("-")
            field_name = field[1:] if is_desc else field

            # Handle field.subfield notation for relationship sorting
            if "." in field_name and not hasattr(self.model, field_name):
                parts = field_name.split(".")
                if len(parts) == 2 and hasattr(self.model, parts[0]):
                    relationship = getattr(self.model, parts[0])
                    if hasattr(relationship.property.mapper.class_, parts[1]):
                        related_field = getattr(relationship.property.mapper.class_, parts[1])
                        order_field = related_field.desc() if is_desc or sort_desc else related_field
                        query = query.join(relationship.property.mapper.class_).order_by(order_field)
                        continue

            # Regular field sorting
            if hasattr(self.model, field_name):
                order_field = getattr(self.model, field_name)
                if is_desc or sort_desc:
                    query = query.order_by(order_field.desc())
                else:
                    query = query.order_by(order_field)
            else:
                logger.warning(f"Sort field {field_name} not found in model {self.model.__name__}")

        return query

    def process_query_results(self, result, output_filters: List[str] | None = None):
        """Process query results based on output filters."""
        if output_filters and any(hasattr(self.model, field) for field in output_filters):
            # When selecting specific columns, result will be tuples
            rows_result = result.all()
            valid_filters = [f for f in output_filters if hasattr(self.model, f)]

            # Convert to dictionaries if specific columns were requested
            return [
                {valid_filters[i]: value for i, value in enumerate(row) if i < len(valid_filters)}
                for row in rows_result
            ]
        else:
            # Normal case - full model objects
            return result.scalars().all()


class BaseDAO(Generic[DataObject]):
    # Subclasses must assign the model class.
    model: Type[DataObject]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.query_helper = QueryHelper(self.model)
        logger.debug("Initialized BaseDAO for model: {}", self.model.__name__)

    async def pre_create_hook(self, obj: DataObject) -> None:
        """Hook for subclasses to modify obj before creation."""
        pass

    async def pre_update_hook(self, entity: DataObject) -> None:
        """Hook for subclasses to modify entity before updating."""
        pass

    async def get(self, id: int) -> Optional[DataObject]:
        logger.debug("Fetching {} with id: {}", self.model.__name__, id)
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        obj = result.scalars().first()
        if obj:
            logger.debug("Found {}: {}", self.model.__name__, obj)
        else:
            logger.debug("{} with id {} not found", self.model.__name__, id)
        return obj

    async def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        search_filters: Dict[str, Any] | None = None,
        output_filters: List[str] | None = None,
        sort_by: str | None = "id",
        sort_desc: bool | None = False,
    ) -> Tuple[List[Optional[DataObject]], int, int]:
        """
        Get all/filtered models with limit/offset pagination.

        :param limit: Limit of rows.
        :param offset: Offset of rows.
        :param search_filters: Dictionary to filter by columns and values.
        :param output_filters: List of column names to include in the output.
        :param sort_by: Column name to sort the results by.
        :param sort_desc: Whether to sort in descending order or not.
        :return: A tuple containing the challenge list, total pages, and total record count.
        """
        logger.debug("Fetching all entities of {}", self.model.__name__)

        # Step 1: Create base query with output filters
        query = self.query_helper.build_query_with_output_filters(output_filters)

        # Step 2: Apply search filters
        query, base_query_for_count = self.query_helper.apply_search_filters(query, search_filters)

        # Step 3: Apply sorting
        query = self.query_helper.apply_sorting(query, sort_by, sort_desc)

        # Step 4: Apply pagination only if limit is provided
        if limit is not None and limit > 0:
            query = query.offset(offset or 0).limit(limit)

        # Step 5: Execute query and process results
        result = await self.session.execute(query)
        rows = self.query_helper.process_query_results(result, output_filters)

        # Step 6: Get total count for pagination
        count_query = select(func.count()).select_from(base_query_for_count.subquery())
        total_records = (await self.session.execute(count_query)).scalar() or 0

        # Step 7: Calculate total pages (1 page if no limit is set)
        if limit is None:
            total_pages = 1
        else:
            total_pages = math.ceil(total_records / limit) if limit > 0 else 1

        return rows, total_pages, total_records

    async def delete(self, id: int) -> None:
        logger.debug("Deleting {} with id: {}", self.model.__name__, id)
        obj = await self.get(id)
        if not obj:
            logger.error("{} with id {} not found for deletion.", self.model.__name__, id)
            raise NoResultFound(f"{str(self.model.__name__).replace('Model', '')} with id {id} not found for deletion.")
        await self.session.delete(obj)

        try:
            await self.session.commit()
            logger.info("{} with id {} deleted successfully.", self.model.__name__, id)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error("Error deleting {} with id {}: {}", self.model.__name__, id, e)
            raise Exception(f"Error deleting {self.model.__name__}") from e
        except Exception as e:
            logger.error("Error deleting {} with id {}: {}", self.model.__name__, id, e)
            raise Exception(f"Error deleting {self.model.__name__}") from e

    async def create_obj(self, obj: Dict) -> DataObject:
        await self.pre_create_hook(obj)
        logger.debug("Creating new {}: {}", self.model.__name__, obj)
        self.session.add(obj)
        try:
            await self.session.commit()
            logger.info("Creating new {}: {}", self.model.__name__, obj)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error("Error creating {}: {}", self.model.__name__, e)
            raise Exception(f"Error creating {self.model.__name__}") from e
        except Exception as e:
            await self.session.rollback()
            logger.error("Error creating {}: {}", self.model.__name__, e)
            raise Exception(f"Error creating {self.model.__name__}") from e
        await self.session.refresh(obj)
        return obj

    async def update_obj(self, obj: DataObject) -> DataObject:
        logger.debug("Updating {}: {}", self.model.__name__, obj)

        self.session.add(obj)
        try:
            await self.session.commit()
            logger.info("Updated {}: {}", self.model.__name__, obj)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error("Error updating {}: {}", self.model.__name__, e)
            raise Exception(f"Error updating {self.model.__name__}") from e
        except Exception as e:
            await self.session.rollback()
            logger.error("Error updating {}: {}", self.model.__name__, e)
            raise Exception(f"Error updating {self.model.__name__}") from e
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Dict) -> DataObject:
        entity: Optional[DataObject] = await self.get(id)
        if not entity:
            logger.error("{} with id {} not found for update: {}", self.model.__name__, id)
            raise NoResultFound("{} with id {} not found for update: {}", self.model.__name__, id)

        # Iterate over the obj and update attributes on the SQLAlchemy model.
        for key, value in obj.items():
            if value is not None and hasattr(entity, key):
                setattr(entity, key, value)

        await self.pre_update_hook(entity)
        updated = await self.update_obj(entity)

        return updated
