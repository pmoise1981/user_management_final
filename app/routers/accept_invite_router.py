# app/routers/accept_invite_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.invite_model import Invite
from settings.config import get_settings
from starlette.responses import RedirectResponse

router = APIRouter(prefix="/accept-invite", tags=["Invites"])

@router.get("/{token}")
async def accept_invite(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invite).where(Invite.token == token))
    invite = result.scalar_one_or_none()

    if not invite:
        raise HTTPException(status_code=404, detail="Invalid or expired invite token")

    if invite.accepted:
        raise HTTPException(status_code=400, detail="Invite has already been accepted")

    invite.accepted = True
    await db.commit()

    forward_url = get_settings().FORWARD_URL
    return RedirectResponse(url=forward_url, status_code=302)

