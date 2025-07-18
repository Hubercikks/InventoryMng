from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from auth.auth import get_user
import models.product
from database import SessionLocal
from schemas.product import product_create
from models import product

router = APIRouter(
    prefix='/api',
    tags=['product_creation']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/creation", response_model=product_create.ProductCreate)
async def product_creation(product_c: product_create.ProductCreate, db: db_dependency, current_user: dict = Depends(get_user)):
    products = db.query(product.Product).filter(product.Product.p_name == product_c.p_name).first()
    if products:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The resource {product_c.p_name} already exists!")
    new_product = product.Product(
        p_name=product_c.p_name,
        category=product_c.category,
        price=product_c.price,
        quantity=product_c.quantity,
        created_by=current_user['uid']
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
