from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Invite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    qr_code_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    accepted = Column(Boolean, default=False)  
