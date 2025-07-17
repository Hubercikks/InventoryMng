from pydantic import BaseModel, conint


class ProductDelete(BaseModel):
    p_id: conint(ge=0)

    class Config:
        schema_extra = {
            "example": {
                "p_id": 3
            }
        }
