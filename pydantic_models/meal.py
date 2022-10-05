# coding: utf-8
from __future__ import annotations

from pydantic_models.orm_base import OrmBase


class MealLiteModel(OrmBase):
    name: str
    user_id: int


class MealFullModel(MealLiteModel):
    user: UserLiteModel
    dishes: list[DishLiteModel]


# =============================================================================


from pydantic_models.user import UserLiteModel
from pydantic_models.dish import DishLiteModel

MealFullModel.update_forward_refs()
