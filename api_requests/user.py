# coding: utf-8
from fastapi import HTTPException
from starlette import status

from api_requests.app import app, db
from api_requests.templates import delete_item, get_all_items, get_item
from database.models import User
from pydantic_models.user import UserLiteModel, UserFullModel


@app.get("/users", response_model=list[UserLiteModel], status_code=200)
def get_all_users():
    return get_all_items(User)


@app.get("/user/{user_id}", response_model=UserFullModel, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    return get_item(User, user_id)  # TODO change response_model (without password)


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    return delete_item(User, user_id)


@app.post("/users", response_model=UserLiteModel, status_code=status.HTTP_201_CREATED)
def create_user(user: UserLiteModel):
    db_user = db.query(User).filter(User.name == user.name).first()

    if db_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,  # TODO change response_model (without password)
    )

    db.add(new_user)
    db.commit()

    return new_user


@app.put("/user/{user_id}", response_model=UserLiteModel, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserLiteModel):
    user_to_update = db.query(User).filter(User.id == user_id).first()

    if not user_to_update:
        raise HTTPException(status_code=400, detail="User does not exist")

    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.password = user.password  # TODO change response_model (without password)

    db.commit()

    return user_to_update
