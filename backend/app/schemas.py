from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class FeedbackCreate(BaseModel):
    product: str
    text: str