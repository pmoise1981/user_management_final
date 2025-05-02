import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.invite_service import InviteService
from app.schemas.invite_schema import InviteCreate
from app.models.invite_model import Invite


@pytest.fixture
def sample_invite_data():
    return InviteCreate(email="test@example.com")


@pytest.mark.asyncio
async def test_create_invite(db_session: AsyncSession, sample_invite_data):
    invite = await InviteService.create_invite(db_session, sample_invite_data)

    assert isinstance(invite, Invite)
    assert invite.email == sample_invite_data.email
    assert invite.token is not None
    assert invite.qr_code_url is not None
    assert invite.qr_code_url.endswith(".png")


@pytest.mark.asyncio
async def test_get_invite_by_token(db_session: AsyncSession, sample_invite_data):
    created_invite = await InviteService.create_invite(db_session, sample_invite_data)
    fetched_invite = await InviteService.get_invite_by_token(db_session, created_invite.token)

    assert fetched_invite is not None
    assert fetched_invite.id == created_invite.id
    assert fetched_invite.token == created_invite.token

