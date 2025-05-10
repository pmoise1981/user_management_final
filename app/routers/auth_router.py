# app/routers/auth_router.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.services.jwt_service import create_access_token
from app.services.user_service import UserService  # ✅ Use the class, not a missing function
from app.dependencies import get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.login_user(db, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401: Incorrect email or password."
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

