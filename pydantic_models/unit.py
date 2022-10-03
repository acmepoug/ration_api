# coding: utf-8
from __future__ import annotations

from pydantic_models.orm_base import OrmBase


class UnitLiteModel(OrmBase):
    name: str


class UnitFullModel(UnitLiteModel):
    portions: list[PortionLiteModel]


# =============================================================================

from pydantic_models.portion import PortionLiteModel

UnitFullModel.update_forward_refs()
