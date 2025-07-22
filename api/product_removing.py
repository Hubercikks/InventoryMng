from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from auth.auth import get_user
from models import product
from services.load_db import get_db
router = APIRouter(
    prefix='/api',
    tags=['remove']
)


get_db()


db_dependency = Annotated[Session, Depends(get_db)]


@router.delete('/product/{product_id}')
async def remove(product_id: int, db:db_dependency, current_user: dict=Depends(get_user)):
    exist = db.query(product.Product).filter(product.Product.p_id == product_id).first()
    if not current_user or current_user['role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can delete products"
        )
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} doesn't exist!"
        )
    db.delete(exist)
    db.commit()
    return f"Product {product_id} have been removed"
