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

class Meal(BaseModel):
    __tablename__ = "meals"

    name = Column(String(100))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, )
    user = relationship("User", back_populates="meals", )

    dishes = relationship(
        "Dish", secondary=t_connect_meal_dish, back_populates="meals", lazy="dynamic",
    )

    def add_dish(self, dish: Dish) -> None:
        if dish not in self.dishes.all():
            self.dishes.append(dish)

    def add_portion_as_dish(self, portion: Portion) -> None:
        new_dish = Dish(name=portion.title, user_id=self.user_id)
        new_dish.add_portion(portion)
        self.add_dish(new_dish)

    def add_to_meal(self, item: Union[Dish, Portion]) -> None:
        if isinstance(item, Dish):
            self.add_dish(item)
        elif isinstance(item, Portion):
            self.add_portion_as_dish(item)
