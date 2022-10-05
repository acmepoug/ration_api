# coding: utf-8
from fastapi import HTTPException
from starlette import status

from api_requests.app import db


def delete_item(item_class, item_id: int):
    item_to_delete = db.query(item_class).filter(item_class.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_class.__name__} Not Found",
        )

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete


def get_all_items(class_item):
    return db.query(class_item).all()


def get_item(item_class, item_id):
    return db.query(item_class).filter(item_class.id == item_id).first()
