from app.schemas.invite_schema import InviteCreate, InviteResponse
from datetime import datetime
import pytest

def test_invite_create_schema():
    data = {"email": "invite@example.com"}
    schema = InviteCreate(**data)

    assert schema.email == "invite@example.com"

def test_invite_response_schema():
    now = datetime.utcnow()
    data = {
        "id": 1,
        "email": "invite@example.com",
        "token": "abc123",
        "qr_code_url": "temp_qrcodes/invite_1.png",
        "created_at": now
    }
    schema = InviteResponse(**data)

    assert schema.id == 1
    assert schema.email == "invite@example.com"
    assert schema.token == "abc123"
    assert schema.qr_code_url.endswith(".png")
    assert isinstance(schema.created_at, datetime)

def test_invite_response_schema_missing_fields():
    with pytest.raises(Exception):
        InviteResponse(id=2, email="x@x.com", token="123")  # missing created_at

