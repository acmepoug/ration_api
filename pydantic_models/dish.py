# coding: utf-8
from __future__ import annotations

from pydantic_models.orm_base import OrmBase


class DishLiteModel(OrmBase):
    name: str
    user_id: int


class DishFullModel(DishLiteModel):
    user: UserLiteModel
    meals: list[MealLiteModel]
    portions: list[PortionLiteModel]


# =============================================================================


from pydantic_models.user import UserLiteModel
from pydantic_models.meal import MealLiteModel
from pydantic_models.portion import PortionLiteModel

DishFullModel.update_forward_refs()
