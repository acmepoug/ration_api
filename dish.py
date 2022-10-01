# coding: utf-8
from fastapi import HTTPException
from sqlalchemy import and_
from starlette import status

from api_requests.app import app, db
from api_requests.templates import delete_item, get_all_items, get_item
from database.models import Dish
from pydantic_models.dish import DishLiteModel, DishFullModel


@app.get("/dishes", response_model=list[DishLiteModel], status_code=200)
def get_all_dishes():
    return get_all_items(Dish)


@app.get("/dish/{dish_id}", response_model=DishFullModel, status_code=status.HTTP_200_OK)
def get_dish(dish_id: int):
    return get_item(Dish, dish_id)


@app.delete("/dish/{dish_id}")
def delete_dish(dish_id: int):
    return delete_item(Dish, dish_id)


@app.post("/dishes", response_model=DishLiteModel, status_code=status.HTTP_201_CREATED)
def create_dish(dish: DishLiteModel):
    db_dish = (
        db.query(Dish)
        .filter(and_(Dish.name == dish.name, Dish.user_id == dish.user_id))
        .first()
    )

    if db_dish is not None:
        raise HTTPException(status_code=400, detail="Dish already exists")

    new_dish = Dish(
        name=dish.name,
        user_id=dish.user_id,
    )

    db.add(new_dish)
    db.commit()

    return new_dish


@app.put("/dish/{dish_id}", response_model=DishLiteModel, status_code=status.HTTP_200_OK)
def update_dish(dish_id: int, dish: DishLiteModel):
    dish_to_update = db.query(Dish).filter(Dish.id == dish_id).first()

    if not dish_to_update:
        raise HTTPException(status_code=400, detail="Dish does not exist")

    dish_to_update.name = dish.name

    db.commit()

    return dish_to_update
