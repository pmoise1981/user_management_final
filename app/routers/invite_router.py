from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.invite_schema import InviteCreate, InviteResponse
from app.services.invite_service import InviteService
from app.dependencies import get_current_active_user, get_db
from app.models.user_model import User

router = APIRouter(prefix="/invites", tags=["Invites"])

@router.post("/", response_model=InviteResponse)
async def create_invite(
    invite_data: InviteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        invite = await InviteService.create_invite(db, invite_data)
        return invite  # ✅ Return model instance directly
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{invite_id}", response_model=InviteResponse)
async def get_invite(invite_id: int, db: AsyncSession = Depends(get_db)):
    invite = await InviteService.get_invite(db, invite_id)
    if not invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    return invite  # ✅ Return model instance directly

