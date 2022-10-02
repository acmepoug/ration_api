# coding: utf-8
from fastapi import HTTPException
from sqlalchemy import and_
from starlette import status

from api_requests.app import app, db
from api_requests.templates import delete_item, get_all_items, get_item
from database.models import Portion
from pydantic_models.portion import PortionLiteModel, PortionFullModel


@app.get("/portions", response_model=list[PortionLiteModel], status_code=200)
def get_all_portions():
    return get_all_items(Portion)


@app.get(
    "/portion/{portion_id}",
    response_model=PortionFullModel,
    status_code=status.HTTP_200_OK,
)
def get_portion(portion_id: int):
    return get_item(Portion, portion_id)


@app.delete("/portion/{portion_id}")
def delete_portion(portion_id: int):
    return delete_item(Portion, portion_id)


@app.post("/portions", response_model=PortionLiteModel, status_code=status.HTTP_201_CREATED)
def create_portion(portion: PortionLiteModel):
    db_portion = (
        db.query(Portion)
        .filter(
            and_(
                Portion.value == portion.value,
                Portion.product_id == portion.product_id,
                Portion.unit_id == portion.unit_id,
                Portion.user_id == portion.user_id,
            )
        )
        .first()
    )

    if db_portion is not None:
        raise HTTPException(status_code=400, detail="Portion already exists")

    new_portion = Portion(
        value=portion.value,
        product_id=portion.product_id,
        unit_id=portion.unit_id,
        user_id=portion.user_id,
    )

    db.add(new_portion)
    db.commit()

    return new_portion


@app.put(
    "/portion/{portion_id}",
    response_model=PortionLiteModel,
    status_code=status.HTTP_200_OK,
)
def update_portion(portion_id: int, portion: PortionLiteModel):
    portion_to_update = db.query(Portion).filter(Portion.id == portion_id).first()

    if not portion_to_update:
        raise HTTPException(status_code=400, detail="Portion does not exist")

    portion_to_update.value = portion.value
    portion_to_update.product_id = portion.product_id
    portion_to_update.unit_id = portion.unit_id
    db.commit()

    return portion_to_update
