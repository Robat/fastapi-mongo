from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    hashed_password: str

    class Config:
        orm_mode = True
