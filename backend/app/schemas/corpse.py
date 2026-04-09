from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class CorpseStatus(str, Enum):
    Needs_Head = 'Needs_Head'
    Needs_Torso = 'Needs_Torso'
    Needs_Legs = 'Needs_Legs'
    Completed = 'Completed'

class CorpseBase(BaseModel):
    is_locked: Optional[bool] = False

class CorpseCreate(CorpseBase):
    status: Optional[CorpseStatus] = CorpseStatus.Needs_Head

class CorpseUpdate(CorpseBase):
    status: Optional[CorpseStatus] = None
    head_url: Optional[str] = None
    torso_url: Optional[str] = None
    legs_url: Optional[str] = None
    final_image_url: Optional[str] = None
    is_locked: Optional[bool] = None

class CorpseInDBBase(CorpseBase):
    id: int
    status: CorpseStatus
    head_url: Optional[str] = None
    torso_url: Optional[str] = None
    legs_url: Optional[str] = None
    final_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Corpse(CorpseInDBBase):
    pass

class SegmentSubmission(BaseModel):
    image_data: str  # Base64 encoded PNG representation of the segment drawn
