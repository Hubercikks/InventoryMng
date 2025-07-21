from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from schemas.product import product_update
from auth.auth import get_user
from models import product
from services.load_db import get_db

router = APIRouter(
    prefix='/api',
    tags=['update']
)

get_db()

db_dependency = Annotated[Session, Depends(get_db)]


@router.put('/products/{product_id}', status_code=200)
async def update_product(
    product_id: int,
    product_u: product_update.ProductUpdate,
    db: db_dependency,
    current_user: dict = Depends(get_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized for this operation"
        )

    existing = db.query(product.Product).filter(product.Product.p_id == product_id).first()

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not exist"
        )

    for key, value in product_u.dict(exclude_unset=True).items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing

