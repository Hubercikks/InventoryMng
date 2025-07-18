from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    role: str
    message: str

    model_config = {
        "from_attributes": True
    }
