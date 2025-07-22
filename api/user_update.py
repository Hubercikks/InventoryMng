from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.load_db import get_db
from schemas.user import user_update_scheme
from auth.auth import get_user
from models import user

router = APIRouter(
    prefix='/api',
    tags=['users']
)

get_db()


db_dependency = Annotated[Session, Depends(get_db)]


@router.put("/user/{user_id}", status_code=200)
async def user_put(user_id: int, user_u: user_update_scheme.UserUpdate, db: db_dependency, current_user: dict=Depends(get_user)):

    if not (current_user['role'] == 'admin'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can update user accounts"
        )
    exist = db.query(user.User).filter(user.User.id == user_id).first()
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    if user_u.email and user_u.email != exist.email:
        email_in_use = db.query(user.User).filter(user.User.email == user_u.email).first()
        if email_in_use:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {user_u.email} is already taken"
            )
    for key, value in user_u.dict(exclude_unset=True).items():
        setattr(exist, key, value)

    db.commit()
    db.refresh(exist)

    return exist

