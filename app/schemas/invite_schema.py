from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class InviteCreate(BaseModel):
    email: EmailStr

class InviteResponse(BaseModel):
    id: int
    email: EmailStr
    token: str
    qr_code_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

