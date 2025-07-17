from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from typing_extensions import Annotated
from schemas.user import user_create, user_out, user_login
from schemas.product import product_create, product_delete, product_update
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import product, user
from passlib.context import CryptContext


app = FastAPI()
router = APIRouter()
user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/createuser/", status_code=status.HTTP_201_CREATED, response_model=user_out)
async def create_user(user: user_create.UserCreate, db: db_dependency):
    existing = db.query(user.User).filter(user.User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with this e-mail address already exists"
        )
