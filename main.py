from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from auth import auth
from database import engine, SessionLocal
from models import product, user
from schemas.user import user_out
from api import product_creation, product_removing

app = FastAPI()
user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_dependency() -> Annotated[Session, Depends(get_db)]:
    return "Hello"


@app.get("/me", response_model=user_out.UserOut)
async def read_users_me(current_user: dict = Depends(auth.get_user), db: Session = Depends(get_db)):
    user_e = db.query(user.User).filter(user.User.email == current_user['email']).first()
    if not user_e:
        raise HTTPException(status_code=404, detail="User not found")
    return user_e


app.include_router(auth.router)
app.include_router(product_creation.router)
app.include_router(product_removing.router)
