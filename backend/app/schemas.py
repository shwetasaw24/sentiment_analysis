# app/schemas.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class FeedbackCreate(BaseModel):
    product: str
    text: str

class FeedbackResponse(BaseModel):
    id: int
    product: str
    text: str
    positive_prob: float
    negative_prob: float
    sentiment: str

    class Config:
        orm_mode = True