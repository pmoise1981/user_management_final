from fastapi import APIRouter
from . import user_routes, invite_router

api_router = APIRouter()
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(invite_router.router, prefix="/invites", tags=["invites"])

