from datetime import datetime
from pathlib import Path
import qrcode

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.invite_model import Invite
from app.schemas.invite_schema import InviteCreate, InviteResponse
from app.utils.token_generator import generate_token
from app.utils.minio_client import upload_qr_to_minio
from app.dependencies import get_db, get_current_user
from settings.config import settings

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong"}

class InviteService:
    @staticmethod
    async def create_invite(db: AsyncSession, invite_data: InviteCreate, inviter):
        token = generate_token()

        new_invite = Invite(
            email=invite_data.email,
            token=token,
            inviter_id=inviter.id
        )

        db.add(new_invite)
        await db.flush()

        # Generate QR Code
        qr_filename = f"invite_{new_invite.id}.png"
        qr_path = Path(settings.qr_code_dir) / qr_filename
        qr_path.parent.mkdir(parents=True, exist_ok=True)

        img = qrcode.make(token)
        img.save(qr_path)

        # Upload to MinIO
        qr_code_url = upload_qr_to_minio(qr_path, f"qr_codes/{qr_filename}")
        new_invite.qr_code_url = qr_code_url

        await db.commit()
        await db.refresh(new_invite)
        return new_invite

    @staticmethod
    async def get_invite(db: AsyncSession, invite_id: int):
        result = await db.execute(select(Invite).where(Invite.id == invite_id))
        return result.scalars().first()

    @staticmethod
    async def accept_invite(db: AsyncSession, token: str):
        result = await db.execute(select(Invite).where(Invite.token == token))
        invite = result.scalar_one_or_none()

        if not invite or invite.accepted:
            return None

        invite.accepted = True
        invite.accepted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(invite)
        return invite

# ✅ THIS was incorrectly indented earlier — it must be outside the class
@router.post("/", response_model=InviteResponse)
async def create_invite_endpoint(
    invite_data: InviteCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        invite = await InviteService.create_invite(db, invite_data, current_user)
        return invite
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


