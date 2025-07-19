from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from auth.auth import get_user
import models.product
from database import SessionLocal
from schemas.product import product_delete
from models import product

router = APIRouter(
    prefix='/api',
    tags=['product_removing']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.delete('/product_removing')
async def remove(product_r: product_delete.ProductDelete, db:db_dependency, current_user: dict=Depends(get_user)):
    exist = db.query(product.Product).filter(product.Product.p_id == product_r.p_id).first()
    if exist:
        db.delete(exist)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Product with id {product_r.p_id} have been removed!"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_r.p_id} doesn't exist!"
    )
