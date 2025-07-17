from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing_extensions import Annotated
import models.user
from database import engine, SessionLocal
from models import product, user
from schemas.user import user_create, user_out

app = FastAPI()
router = APIRouter()
user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/createuser/", status_code=status.HTTP_201_CREATED, response_model=user_out.UserOut)
async def create_user(user_in: user_create.UserCreate, db: db_dependency):
    existing = db.query(user.User).filter(user.User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with this e-mail address already exists"
        )
    hashed_password = pwd.hash(user_in.password)

    new_user = models.user.User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
app.include_router(router)
