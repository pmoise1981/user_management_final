from sqlalchemy import delete
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate
from app.services.user_service import UserService
import pytest

class DummyEmailService:
    async def send_verification_email(self, user):
        pass  # Do nothing in test

@pytest.fixture
async def users_with_same_role_50_users(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()

    for i in range(50):
        user_data = {
            "nickname": f"testuser{i}",
            "email": f"user{i}@example.com",
            "first_name": "Test",
            "last_name": f"User{i}",
            "password": "TestPassword123!"
        }

        await UserService.create(
            session=db_session,
            user_data=user_data,
            email_service=DummyEmailService()
        )

    await db_session.commit()

