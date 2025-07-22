from sqlalchemy import Integer, String, Column, Float, ForeignKey, NUMERIC, DateTime
from database import Base
from datetime import datetime


class Product(Base):
    __tablename__ = 'products'

    p_id = Column(Integer, index=True, primary_key=True)
    p_name = Column(String(255), index=True)
    category = Column(String(100), index=True)
    price = Column(NUMERIC)
    quantity = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
