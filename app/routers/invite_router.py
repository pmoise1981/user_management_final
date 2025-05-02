from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.invite_schema import InviteCreate, InviteResponse
from app.services.invite_service import InviteService
from app.dependencies import get_current_active_user
from app.models.user_model import User

router = APIRouter(prefix="/invites", tags=["Invites"])

@router.post("/", response_model=InviteResponse)
async def create_invite(
    invite_data: InviteCreate,
    current_user: User = Depends(get_current_active_user),
):
    try:
        invite = await InviteService.create_invite(invite_data, created_by=current_user.id)
        return invite
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{invite_id}", response_model=InviteResponse)
async def get_invite(invite_id: int):
    invite = await InviteService.get_invite(invite_id)
    if not invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    return invite

