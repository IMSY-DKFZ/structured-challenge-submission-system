from typing import Any, Dict, Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# 1. Requests
class SearchRequest(BaseModel):
    search_filters: Dict[str, Any] | None = Field(
        default=None,
        title="Dictionary containing column names as keys and values to filter on search (optional).",
        examples=[
            {
                "id": "1",
                "field": "some text",
                "field__startswith": "some text",
                "field__endswith": "some text",
                "field__contains": "some text",
                "field__like": "some text",
                "field__ilike": "some text",
                "field__lt": "2022-01-01T00:00:00Z",
                "field__between": [
                    "2021-01-01T00:00:00Z",
                    "2021-12-31T23:59:59Z",
                ],
            }
        ],
    )
    output_filters: List[str] | None = Field(
        default=None,
        title="Dictionary containing column names as keys and values to filter on output (optional).",
        examples=[["challenge_name", "challenge_status"]],
    )
    # select_columns: List[str] | None = Field(
    #     default=None,
    #     title="--CURRENTLY NOT WORKING-- List of columns to be selected in the result (optional).",
    # )


class SearchRequestChallenge(SearchRequest):
    """
    Extended SearchRequest model for challenge search.
    This model includes optional 'output_filters_task' to filter task object inside of
    challenge object.
    """

    output_filters_task: List[str] | None = Field(
        default=None,
        title="Dictionary containing column names as keys and values to filter on task object (optional).",
    )


# 2. Responses
class PaginationResponse(BaseModel, Generic[T]):
    """The response for a pagination query."""

    total_pages: int | None = None
    total_records: int | None = None
    content: List[T] | None = None


class BulkOperationResponse(BaseModel, Generic[T]):
    """
    Generic response model for bulk operations.

    Type Parameters:
        T: The model type for successful operations

    Attributes:
        successful: List of successfully processed entities
        failed: List of failed operations with error details
    """

    detail: str | None = None
    successful: List[T] | Dict[str, Any] = None
    failed: List[Dict[str, Any]] | Dict[str, Any] = None
