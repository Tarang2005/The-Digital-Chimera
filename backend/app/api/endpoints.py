from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.corpse import Corpse
from app.services.storage import save_base64_image, UPLOAD_DIR
import redis
from app.core.config import settings
import uuid
import base64
from io import BytesIO
from PIL import Image
import os

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

LOCK_TTL = 900  # 15 minutes

class SegmentPayload(BaseModel):
    session_id: str
    segment_type: str
    image_data: str # Base64 PNG

@router.get("/get-turn")
def get_turn(db: Session = Depends(get_db)):
    # 1. Prefer incomplete corpses
    for target_status in ["Needs_Head", "Needs_Torso", "Needs_Legs"]:
        corpse = db.query(Corpse).filter(Corpse.status == target_status, Corpse.is_locked == False).first()
        if corpse:
            lock_key = f"lock:corpse_{corpse.id}"
            if not redis_client.exists(lock_key):
                session_id = str(uuid.uuid4())
                redis_client.setex(lock_key, LOCK_TTL, session_id)
                corpse.is_locked = True
                db.commit()
                
                sliver_url = None
                if target_status == "Needs_Torso" and corpse.head_url:
                    # In this setup, we assume sliver exists as sliver_{id}.png in the uploads path
                    sliver_url = f"/uploads/sliver_{corpse.id}_head.png"
                elif target_status == "Needs_Legs" and corpse.torso_url:
                    sliver_url = f"/uploads/sliver_{corpse.id}_torso.png"

                return {
                    "corpse_id": corpse.id,
                    "target_segment": target_status,
                    "session_id": session_id,
                    "sliver_url": sliver_url
                }

    # 2. If no available corpses, create a new one
    new_corpse = Corpse(status="Needs_Head", is_locked=True)
    db.add(new_corpse)
    db.commit()
    db.refresh(new_corpse)
    
    session_id = str(uuid.uuid4())
    redis_client.setex(f"lock:corpse_{new_corpse.id}", LOCK_TTL, session_id)
    
    return {
        "corpse_id": new_corpse.id,
        "target_segment": "Needs_Head",
        "session_id": session_id,
        "sliver_url": None
    }

@router.post("/submit-segment/{corpse_id}")
def submit_segment(
    corpse_id: int, 
    payload: SegmentPayload,
    db: Session = Depends(get_db)
):
    lock_key = f"lock:corpse_{corpse_id}"
    current_session = redis_client.get(lock_key)
    
    if current_session != payload.session_id:
        raise HTTPException(status_code=403, detail="Lock expired or invalid session")
        
    corpse = db.query(Corpse).filter(Corpse.id == corpse_id).first()
    if not corpse:
        raise HTTPException(status_code=404, detail="Corpse not found")
        
    # Save main segment locally
    url_path = save_base64_image(payload.image_data, prefix=f"corpse_{corpse_id}_{payload.segment_type}")
    
    # Process "Sliver" using Pillow if Head or Torso
    if payload.segment_type in ["Needs_Head", "Needs_Torso"]:
        try:
            base64_str = payload.image_data.split("base64,")[1] if "base64," in payload.image_data else payload.image_data
            img_data = base64.b64decode(base64_str)
            img = Image.open(BytesIO(img_data)).convert("RGBA")
            
            # The prompt requires: image.crop((0, 480, 500, 500))
            sliver = img.crop((0, 480, 500, 500))
            
            slicer_prefix = "head" if payload.segment_type == "Needs_Head" else "torso"
            sliver_filename = f"sliver_{corpse_id}_{slicer_prefix}.png"
            sliver_filepath = os.path.join(UPLOAD_DIR, sliver_filename)
            
            sliver.save(sliver_filepath, format="PNG")
        except Exception as e:
            print(f"Error processing sliver: {e}")
            raise HTTPException(status_code=500, detail="Failed to process image sliver")

    # Update DB fields
    if payload.segment_type == "Needs_Head":
        corpse.head_url = url_path
        corpse.status = "Needs_Torso"
    elif payload.segment_type == "Needs_Torso":
        corpse.torso_url = url_path
        corpse.status = "Needs_Legs"
    elif payload.segment_type == "Needs_Legs":
        corpse.legs_url = url_path
        corpse.status = "Completed"
            
    # Release Lock
    corpse.is_locked = False
    redis_client.delete(lock_key)
    db.commit()
    
    return {"message": "Success", "status": corpse.status}
