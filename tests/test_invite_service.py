import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.invite_service import InviteService
from app.schemas.invite_schema import InviteCreate
from app.models.invite_model import Invite
from pathlib import Path
import os


@pytest.fixture
def sample_invite_data():
    return InviteCreate(email="test@example.com")


@pytest.mark.asyncio
async def test_create_invite(db_session: AsyncSession, sample_invite_data):
    invite = await InviteService.create_invite(db_session, sample_invite_data)

    assert isinstance(invite, Invite)
    assert invite.email == sample_invite_data.email
    assert invite.token
    assert invite.qr_code_url.endswith(".png")
    assert Path(invite.qr_code_url).exists()


@pytest.mark.asyncio
async def test_get_invite_by_token_found(db_session: AsyncSession, sample_invite_data):
    invite = await InviteService.create_invite(db_session, sample_invite_data)
    result = await InviteService.get_invite_by_token(db_session, invite.token)

    assert result is not None
    assert result.token == invite.token
    assert result.email == invite.email


@pytest.mark.asyncio
async def test_get_invite_by_token_not_found(db_session: AsyncSession):
    result = await InviteService.get_invite_by_token(db_session, "invalid-token-123")
    assert result is None


@pytest.mark.asyncio
async def test_invite_qr_file_saved(db_session: AsyncSession, sample_invite_data):
    invite = await InviteService.create_invite(db_session, sample_invite_data)
    qr_path = Path(invite.qr_code_url)
    assert qr_path.exists()
    assert qr_path.suffix == ".png"


@pytest.mark.asyncio
async def test_multiple_invites_have_unique_tokens(db_session: AsyncSession):
    emails = [f"user{i}@example.com" for i in range(3)]
    tokens = set()
    for email in emails:
        data = InviteCreate(email=email)
        invite = await InviteService.create_invite(db_session, data)
        assert invite.token not in tokens
        tokens.add(invite.token)


@pytest.mark.asyncio
async def test_qr_code_file_cleanup(db_session: AsyncSession, sample_invite_data):
    invite = await InviteService.create_invite(db_session, sample_invite_data)
    path = Path(invite.qr_code_url)
    assert path.exists()
    os.remove(path)
    assert not path.exists()


@pytest.mark.asyncio
async def test_invite_qr_code_url_contains_expected_path(db_session: AsyncSession, sample_invite_data):
    invite = await InviteService.create_invite(db_session, sample_invite_data)
    assert "temp_qrcodes/invite_" in invite.qr_code_url

