from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
from fastapi import status, APIRouter, Depends, HTTPException
from models import user
from schemas.user import user_create, user_out, user_in, user_login
from schemas.token import token
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'SECRET'
ALGORITHM = 'HS256'

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


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

    new_user = user.User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )

    db.add(new_user)
    db.commit()

    return new_user


@router.post("/token", status_code=status.HTTP_200_OK, response_model=token.Token)
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user_e = db.query(user.User).filter(user.User.email == form_data.username).first()
    if not user_e or not pwd.verify(form_data.password, user_e.hashed_password):
        raise HTTPException(status_code=401, detail="Unsuccessful login attempt")
    token_l = create_token(user_e.email, timedelta(minutes=20))
    return {'access_token': token_l, 'token_type': 'bearer', 'message': 'Successfully logged in'}


def create_token(username: str, expires_delta):
    encode = {'sub': username}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user(token_u: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token_u, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'email': email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not Validate user')
