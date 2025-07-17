from sqlalchemy import Integer, String, ForeignKey, Column, VARCHAR, CHAR
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, unique=True)
    hashed_password = Column(VARCHAR(255))
    role = Column(String(50), index=True)
