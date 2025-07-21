from sqlalchemy import Integer, String, Column
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), index=True, nullable=False)
