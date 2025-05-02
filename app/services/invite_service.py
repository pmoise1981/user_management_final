import secrets
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.invite_model import Invite
from app.schemas.invite_schema import InviteCreate
from app.utils.qr_generator import generate_qr_code
# from app.utils.minio_client import upload_file_to_minio  # disabled until MinIO is implemented
from pathlib import Path

class InviteService:
    @staticmethod
    async def create_invite(db: Session, invite_data: InviteCreate) -> Invite:
        token = secrets.token_urlsafe(16)
        invite = Invite(email=invite_data.email, token=token)

        db.add(invite)
        await db.commit()
        await db.refresh(invite)

        # Use a safe default path to store the QR temporarily
        qr_path_str = f"temp_qrcodes/invite_{invite.id}.png"
        qr_path = generate_qr_code(token, qr_path_str)

        # MinIO logic disabled until implemented
        # minio_url = upload_file_to_minio(qr_path)
        # invite.qr_code_url = minio_url
        invite.qr_code_url = qr_path  # temporarily store local path

        await db.commit()
        await db.refresh(invite)

        return invite

    @staticmethod
    async def get_invite_by_token(db: Session, token: str) -> Invite | None:
        result = await db.execute(select(Invite).filter(Invite.token == token))
        return result.scalars().first()

    @staticmethod
    async def get_invite(db: Session, invite_id: int) -> Invite | None:
        result = await db.execute(select(Invite).filter(Invite.id == invite_id))
        return result.scalars().first()

