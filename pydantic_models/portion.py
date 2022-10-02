# coding: utf-8
from __future__ import annotations

from pydantic_models.orm_base import OrmBase


class PortionLiteModel(OrmBase):
    value: int
    unit_id: int
    product_id: int
    user_id: int


class PortionFullModel(PortionLiteModel):
    product: ProductLiteModel
    dishes: list[DishLiteModel]
    user: UserLiteModel
    unit: UnitLiteModel


# =============================================================================


from pydantic_models.user import UserLiteModel
from pydantic_models.dish import DishLiteModel
from pydantic_models.product import ProductLiteModel
from pydantic_models.unit import UnitLiteModel

PortionFullModel.update_forward_refs()
