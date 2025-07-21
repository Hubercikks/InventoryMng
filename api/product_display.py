from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from services.load_db import get_db
from models import product
from auth.auth import get_user

router = APIRouter(
    prefix='/api',
    tags=['products']
)

get_db()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/list', status_code=status.HTTP_200_OK)
async def product_list(db: db_dependency, current_user: dict = Depends(get_user)):
    products = db.query(product.Product).all()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized for this operation"
        )
    return products
