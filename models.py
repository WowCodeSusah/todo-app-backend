from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
    
class Tasks(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key=True, nullable=False)
    task = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False)
    isEditing = Column(Boolean, nullable=False)
    timeCreated = Column(DateTime(timezone=True), server_default=func.now())
    