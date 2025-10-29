from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database_manager import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String, index=True)
    recipient_id = Column(String, index=True)
    message = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
