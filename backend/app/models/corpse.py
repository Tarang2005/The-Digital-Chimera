from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.db.base_class import Base

class Corpse(Base):
    __tablename__ = "corpses"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum('Needs_Head', 'Needs_Torso', 'Needs_Legs', 'Completed', name='corpse_status'), default='Needs_Head', nullable=False)
    
    head_url = Column(String(2048), nullable=True)
    torso_url = Column(String(2048), nullable=True)
    legs_url = Column(String(2048), nullable=True)
    final_image_url = Column(String(2048), nullable=True)
    
    is_locked = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
