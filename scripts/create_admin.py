import asyncio
from sqlalchemy.future import select
from app.models.user_model import User
from app.database import Database
from app.dependencies import get_settings
from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

settings = get_settings()
Database.initialize(settings.database_url)
async_session = Database.get_session_factory()

async def create_admin_user():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == settings.admin_user))
        existing_user = result.scalars().first()
        if existing_user:
            print("✅ Admin user already exists.")
            return

        admin = User(
            nickname="admin",
            email=settings.admin_user,
            hashed_password=hash_password(settings.admin_password),
            is_active=True,
            is_locked=False,
            role="ADMIN"
        )

        session.add(admin)
        await session.commit()
        print("✅ Admin user created.")

if __name__ == "__main__":
    asyncio.run(create_admin_user())

