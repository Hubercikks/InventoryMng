from typing import Optional
from pydantic import BaseModel


class ProductUpdate(BaseModel):
    p_name: Optional[str]
    category: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "p_name": "Dishwasher BOSH",
                "category": "Household appliances",
                "price": 299.99,
                "quantity": 150
            }
        }