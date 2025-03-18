from sqlalchemy import Column, Integer, String, DateTime, func
from app.data.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "user_schema"}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())