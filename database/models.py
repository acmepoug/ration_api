# coding: utf-8
from __future__ import annotations
from typing import Union
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from database.base import BaseModel, Base, SessionLocal

session = SessionLocal()

t_connect_meal_dish = Table(
    "connect_meal_dish",
    Base.metadata,
    Column("meal_id", ForeignKey("meals.id"), primary_key=True, ),
    Column("dish_id", ForeignKey("dishes.id"), primary_key=True, ),
)
t_connect_dish_portion = Table(
    "connect_dish_portion",
    Base.metadata,
    Column("dish_id", ForeignKey("dishes.id"), primary_key=True, ),
    Column("portion_id", ForeignKey("portions.id"), primary_key=True, ),
)

