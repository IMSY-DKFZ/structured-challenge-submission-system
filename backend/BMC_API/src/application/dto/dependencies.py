from typing import TypeVar

from pydantic import BaseModel, create_model

T = TypeVar("T")


def create_all_optional_model(model_name: str, base_model: BaseModel):
    new_model = create_model(
        model_name,
        __base__=base_model,
        **{k: (v.annotation, None) for k, v in base_model.model_fields.items()},
    )
    return new_model
