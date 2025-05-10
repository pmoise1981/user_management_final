from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: EmailStr  # 👈 Make sure this line uses EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

