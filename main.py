from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from auth import auth
from database import SessionLocal
from models import user
from schemas.user import user_out
from api import product_creation, product_removing, product_display, product_updating, user_display, user_update

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/me", response_model=user_out.UserOut, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: dict = Depends(auth.get_user), db: Session = Depends(get_db)):
    user_e = db.query(user.User).filter(user.User.email == current_user['email']).first()
    if not user_e:
        raise HTTPException(status_code=404, detail="User not found")
    return user_e


app.include_router(auth.router)
app.include_router(product_creation.router)
app.include_router(product_removing.router)
app.include_router(product_display.router)
app.include_router(product_updating.router)
app.include_router(user_display.router)
app.include_router(user_update.router)
