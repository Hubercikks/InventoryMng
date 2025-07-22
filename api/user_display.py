from typing import Annotated
from sqlalchemy.orm import Session
from services.load_db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from auth.auth import get_user
from models import user
router = APIRouter(
    prefix='/api',
    tags=['users']
)

get_db()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/users')
async def users_display(db: db_dependency, current_user: dict = Depends(get_user)):
    if not current_user['role'] == 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can display users"
        )
    users = db.query(user.User).all()
    return users




