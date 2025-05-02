import secrets
from app.models.invite_model import Invite
from app.schemas.invite_schema import InviteCreate
from sqlalchemy.orm import Session
from app.utils.qr_generator import generate_qr_code
# from app.utils.minio_client import upload_file_to_minio

class InviteService:
    @staticmethod
    def create_invite(db: Session, invite_data: InviteCreate) -> Invite:
        token = secrets.token_urlsafe(16)
        invite = Invite(email=invite_data.email, token=token)

        db.add(invite)
        db.commit()
        db.refresh(invite)

        qr_path = generate_qr_code(token, invite.id)

        # If you implement MinIO later, you can uncomment this
        # minio_url = upload_file_to_minio(qr_path.name)
        minio_url = "placeholder-url"  # Replace this later

        invite.qr_code_url = minio_url
        db.commit()
        db.refresh(invite)

        return invite

