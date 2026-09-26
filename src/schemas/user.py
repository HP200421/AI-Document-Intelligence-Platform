from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)

class UserResponse(BaseModel):
    name: str
    email: EmailStr

    model_config=ConfigDict(from_attributes=True)
