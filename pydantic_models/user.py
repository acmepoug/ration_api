# coding: utf-8
from __future__ import annotations

from pydantic_models.orm_base import OrmBase


class UserLiteModel(OrmBase):
    name: str
    email: str
    password: str


class UserFullModel(UserLiteModel):
    products: list[ProductLiteModel]
    portions: list[PortionLiteModel]
    dishes: list[DishLiteModel]
    meals: list[MealLiteModel]


# =============================================================================


from pydantic_models.portion import PortionLiteModel
from pydantic_models.product import ProductLiteModel
from pydantic_models.dish import DishLiteModel
from pydantic_models.meal import MealLiteModel

UserFullModel.update_forward_refs()
