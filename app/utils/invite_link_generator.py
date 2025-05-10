from uuid import uuid4
from urllib.parse import urlencode
from app.dependencies import get_settings

settings = get_settings()

def generate_token(user_id: int) -> str:
    invite_link, token = generate_invite_link(user.id)
    base_url = f"{settings.BASE_URL}/invites/accept"
    query_params = urlencode({"token": token, "user_id": user_id})
    return f"{base_url}?{query_params}", token

