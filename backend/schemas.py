from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    risk_tolerance: float
    loss_aversion_coefficient: float
    overconfidence_score: float

    class Config:
        from_attributes = True