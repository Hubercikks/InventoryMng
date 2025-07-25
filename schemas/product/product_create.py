from pydantic import BaseModel, constr, conint, confloat


class ProductCreate(BaseModel):
    p_name: constr(min_length=1, max_length=100)
    category: constr(min_length=1)
    price: confloat(ge=0)
    quantity: conint(ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "p_name": "Dishwasher BOSH",
                "category": "Household appliances",
                "price": 299.99,
                "quantity": 150
            }
        }

