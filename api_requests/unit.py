# coding: utf-8
from fastapi import HTTPException
from starlette import status

from api_requests.app import app, db
from api_requests.templates import delete_item, get_all_items, get_item
from database.models import Unit
from pydantic_models.unit import UnitLiteModel, UnitFullModel


@app.get("/units", response_model=list[UnitLiteModel], status_code=200)
def get_all_units():
    return get_all_items(Unit)


@app.get("/unit/{unit_id}", response_model=UnitFullModel, status_code=status.HTTP_200_OK)
def get_unit(unit_id: int):
    return get_item(Unit, unit_id)


@app.delete("/unit/{unit_id}")
def delete_unit(unit_id: int):
    return delete_item(Unit, unit_id)


@app.post("/units", response_model=UnitLiteModel, status_code=status.HTTP_201_CREATED)
def create_unit(unit: UnitLiteModel):
    db_unit = db.query(Unit).filter(Unit.name == unit.name).first()

    if db_unit is not None:
        raise HTTPException(status_code=400, detail="Unit already exists")

    new_unit = Unit(
        name=unit.name,
    )

    db.add(new_unit)
    db.commit()

    return new_unit


@app.put("/unit/{unit_id}", response_model=UnitLiteModel, status_code=status.HTTP_200_OK)
def update_unit(unit_id: int, unit: UnitLiteModel):
    unit_to_update = db.query(Unit).filter(Unit.id == unit_id).first()

    if not unit_to_update:
        raise HTTPException(status_code=400, detail="Unit does not exist")

    unit_to_update.name = unit.name

    db.commit()

    return unit_to_update
