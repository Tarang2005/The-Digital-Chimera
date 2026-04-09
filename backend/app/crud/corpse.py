from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.corpse import Corpse
from app.schemas.corpse import CorpseStatus

def get_available_corpse(db: Session) -> Corpse:
    """Finds an available corpse to draw, or creates a new one."""
    corpse = db.query(Corpse).filter(
        Corpse.status != 'Completed',
        Corpse.is_locked == False
    ).first()
    
    if not corpse:
        corpse = Corpse(status='Needs_Head', is_locked=False)
        db.add(corpse)
        db.commit()
        db.refresh(corpse)
        
    return corpse

def lock_corpse(db: Session, corpse_id: int) -> Corpse:
    """Locks a corpse so no one else can draw on it concurrently."""
    corpse = db.query(Corpse).filter(
        Corpse.id == corpse_id,
        Corpse.is_locked == False
    ).first()
    
    if not corpse:
        raise HTTPException(status_code=409, detail="Corpse is no longer available or is locked.")
        
    corpse.is_locked = True
    db.commit()
    db.refresh(corpse)
    return corpse

def submit_segment(db: Session, corpse_id: int, image_url: str) -> Corpse:
    """Updates the corpse with the submitted image and advances its status."""
    corpse = db.query(Corpse).filter(Corpse.id == corpse_id).first()
    
    if not corpse:
        raise HTTPException(status_code=404, detail="Corpse not found")
        
    if not corpse.is_locked:
        raise HTTPException(status_code=400, detail="Corpse must be locked before submitting.")

    if corpse.status == 'Needs_Head':
        corpse.head_url = image_url
        corpse.status = 'Needs_Torso'
    elif corpse.status == 'Needs_Torso':
        corpse.torso_url = image_url
        corpse.status = 'Needs_Legs'
    elif corpse.status == 'Needs_Legs':
        corpse.legs_url = image_url
        corpse.status = 'Completed'
        # In a real app, trigger a "stitch" operation on Completed here
    else:
        raise HTTPException(status_code=400, detail="Corpse is already completed.")

    corpse.is_locked = False
    db.commit()
    db.refresh(corpse)
    return corpse
