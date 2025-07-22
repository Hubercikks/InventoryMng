from pydantic import BaseModel, EmailStr, constr, field_validator
from pydantic_core import PydanticCustomError


class UserUpdate(BaseModel):
    email: EmailStr
    role: constr(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
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
