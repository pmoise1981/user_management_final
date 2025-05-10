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
    accepted: bool                     # ✅ Include accepted field
    accepted_at: Optional[datetime]   # ✅ Include accepted_at field

    class Config:
        from_attributes = True        # ✅ Updated for Pydantic v2

