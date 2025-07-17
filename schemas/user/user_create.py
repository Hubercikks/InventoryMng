from pydantic import BaseModel, EmailStr, constr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    role: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "role": "employee"
            }
        }

    @field_validator('role')
    @classmethod
    def no_digits(cls, r: str) -> str:
        if any(char.isdigit() for char in r):
            raise ValueError("No digits in role allowed")
