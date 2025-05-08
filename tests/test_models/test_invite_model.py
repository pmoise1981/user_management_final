from app.models.invite_model import Invite

def test_invite_model_fields():
    invite = Invite(
        email="test@example.com",
        token="securetoken123",
        qr_code_url="temp_qrcodes/invite_1.png"
    )

    assert invite.__tablename__ == "invites"
    assert invite.email == "test@example.com"
    assert invite.token == "securetoken123"
    assert invite.qr_code_url == "temp_qrcodes/invite_1.png"

