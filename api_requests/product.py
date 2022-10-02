# coding: utf-8
from fastapi import HTTPException
from sqlalchemy import and_
from starlette import status

from api_requests.app import app, db
from api_requests.templates import delete_item, get_all_items, get_item
from database.models import Product
from pydantic_models.product import ProductLiteModel, ProductFullModel


@app.get("/products", response_model=list[ProductLiteModel], status_code=200)
def get_all_products():
    return get_all_items(Product)


@app.get(
    "/product/{product_id}",
    response_model=ProductFullModel,
    status_code=status.HTTP_200_OK,
)
def get_product(product_id: int):
    return get_item(Product, product_id)


@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    return delete_item(Product, product_id)


@app.post("/products", response_model=ProductLiteModel, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductLiteModel):
    db_product = (
        db.query(Product)
        .filter(
            and_(
                Product.name == product.name,
                Product.user_id == product.user_id,
            )
        )
        .first()
    )

    if db_product is not None:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = Product(
        name=product.name,
        protein=product.protein,
        fat=product.fat,
        carbohydrates=product.carbohydrates,
        calories=product.calories,
        user_id=product.user_id,
    )  # TODO Convert to abstract function

    db.add(new_product)
    db.commit()

    return new_product


@app.put(
    "/product/{product_id}",
    response_model=ProductLiteModel,
    status_code=status.HTTP_200_OK,
)
def update_product(product_id: int, product: ProductLiteModel):
    product_to_update = db.query(Product).filter(Product.id == product_id).first()

    if not product_to_update:
        raise HTTPException(status_code=400, detail="Product does not exist")

    product_to_update.name = product.name
    product_to_update.protein = product.protein
    product_to_update.fat = product.fat
    product_to_update.carbohydrates = product.carbohydrates
    product_to_update.calories = product.calories
    db.commit()

    return product_to_update
