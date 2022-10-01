# coding: utf-8
from fastapi import HTTPException
from sqlalchemy import and_
from starlette import status

from api_requests.app import app, db
from api_requests.templates import delete_item, get_all_items, get_item
from database.models import Meal
from pydantic_models.meal import MealLiteModel, MealFullModel


@app.get("/meals", response_model=list[MealLiteModel], status_code=200)
def get_all_meals():
    return get_all_items(Meal)


@app.get("/meal/{meal_id}", response_model=MealFullModel, status_code=status.HTTP_200_OK)
def get_meal(meal_id: int):
    return get_item(Meal, meal_id)


@app.delete("/meal/{meal_id}")
def delete_meal(meal_id: int):
    return delete_item(Meal, meal_id)


@app.post("/meals", response_model=MealLiteModel, status_code=status.HTTP_201_CREATED)
def create_meal(meal: MealLiteModel):
    db_meal = (
        db.query(Meal)
        .filter(
            and_(
                Meal.name == meal.name,
                Meal.user_id == meal.user_id,
            )
        )
        .first()
    )

    if db_meal is not None:
        raise HTTPException(status_code=400, detail="Meal already exists")

    new_meal = Meal(
        name=meal.name,
        user_id=meal.user_id,
    )

    db.add(new_meal)
    db.commit()

    return new_meal


@app.put("/meal/{meal_id}", response_model=MealFullModel, status_code=status.HTTP_200_OK)
def update_meal(meal_id: int, meal: MealLiteModel):
    meal_to_update = db.query(Meal).filter(Meal.id == meal_id).first()

    if not meal_to_update:
        raise HTTPException(status_code=400, detail="Meal does not exist")

    meal_to_update.name = meal.name

    db.commit()

    return meal_to_update
