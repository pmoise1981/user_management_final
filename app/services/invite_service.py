from builtins import Exception
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.invite_model import Invite
from app.schemas.invite_schema import InviteCreate
from app.models.user_model import User
from app.utils.invite_link_generator import generate_token
from app.utils.qr_generator import generate_qr_code
from settings.config import Settings
import os

class InviteService:
    @staticmethod
    async def create_invite(
        db: AsyncSession,
        invite_data: InviteCreate,
        inviter: User,
        settings: Settings = Settings()
    ) -> Invite:
        token = generate_token()
        qr_content = f"{settings.invite_redirect_base_url}/{token}"

        qr_code_filename = f"invite_{inviter.id}_{token}.png"
        qr_code_path = os.path.join(settings.qr_code_dir, qr_code_filename)
        generate_qr_code(qr_content, qr_code_path)

        invite = Invite(
            email=invite_data.email,
            token=token,
            qr_code_url=qr_code_path,
            inviter_id=inviter.id
        )

        db.add(invite)
        await db.commit()
        await db.refresh(invite)
        return invite

    @staticmethod
    async def get_invite(db: AsyncSession, invite_id: int) -> Invite | None:
        result = await db.execute(select(Invite).where(Invite.id == invite_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def accept_invite(db: AsyncSession, token: str) -> bool:
        result = await db.execute(select(Invite).where(Invite.token == token))
        invite = result.scalar_one_or_none()

        if not invite or invite.accepted:
            return False

        await db.execute(
            update(Invite)
            .where(Invite.id == invite.id)
            .values(accepted=True)
        )
        await db.commit()
        return True

