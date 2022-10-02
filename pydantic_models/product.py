# coding: utf-8
from __future__ import annotations

from pydantic_models.orm_base import OrmBase


class ProductLiteModel(OrmBase):
    name: str
    protein: float
    fat: float
    carbohydrates: float
    calories: int
    user_id: int


class ProductFullModel(ProductLiteModel):
    user: UserLiteModel
    portions: list[PortionLiteModel]


# =============================================================================

from pydantic_models.user import UserLiteModel
from pydantic_models.portion import PortionLiteModel

ProductFullModel.update_forward_refs()
