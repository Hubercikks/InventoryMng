from pydantic import BaseModel, EmailStr, constr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    role: constr(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "role": "employee"
            }
        }

