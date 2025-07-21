from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.product import product_update
from auth.auth import get_user
from models import product

router = APIRouter(
    prefix='/api',
    tags=['product_updating']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/product_updating')
async def product_updating(product_u: product_update.ProductUpdate, db: db_dependency,
                           current_user: dict = Depends(get_user)):
    existing = db.query(product.Product).filter(product.Product.p_name == product_u.p_name).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No product named {product_u.p_name}!"
        )
    updated_product = product.Product(
        p_name=product_u.p_name,
        category=product_u.category,
        price=product_u.price,
        quantity=product_u.quantity
    )
    try:
        db.commit()
        db.refresh(updated_product)
    except:
        return "Unexpected error"
