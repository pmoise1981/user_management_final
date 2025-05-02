from uuid import uuid4
from urllib.parse import urlencode
from app.config import settings


def generate_invite_link(user_id: int) -> str:
    token = str(uuid4())
    base_url = f"{settings.BASE_URL}/invites/accept"
    query_params = urlencode({"token": token, "user_id": user_id})
    return f"{base_url}?{query_params}", token

