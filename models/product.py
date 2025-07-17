from sqlalchemy import Integer, String, Column, VARCHAR, Float
from database import Base


class Product(Base):
    __tablename__ = 'products'

    p_id = Column(Integer, index=True, primary_key=True)
    p_name = Column(String(255), index=True)
    category = Column(String(100), index=True)
    price = Column(Integer)
    quantity = Column(Float)
    min_stock = Column(Integer)
