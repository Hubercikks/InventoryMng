from pydantic import BaseModel, EmailStr, constr, field_validator
from pydantic_core import PydanticCustomError

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

    @field_validator('role', mode='before')
    @classmethod
    def check_role(cls, r: str):
        roles = ['employee', 'admin', 'manager']
        if r not in roles:
            raise PydanticCustomError(
                'value_error.invalid_role',
                'Role "{role}" does not exist.',
                {'role': r}
            )
        return r
