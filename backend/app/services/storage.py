import base64
import os
import uuid
from pathlib import Path
from fastapi import HTTPException

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_base64_image(base64_data: str, prefix: str = "segment") -> str:
    """
    Saves a base64 encoded image to the local file system.
    Expects format: 'data:image/png;base64,iVBORw0KGgo...' or just the base64 string.
    Returns the relative URL path to access the image.
    """
    try:
        # Strip header if present
        if "base64," in base64_data:
            base64_data = base64_data.split("base64,")[1]
            
        decoded_data = base64.b64decode(base64_data)
        
        filename = f"{prefix}_{uuid.uuid4().hex}.png"
        file_path = UPLOAD_DIR / filename
        
        with open(file_path, "wb") as f:
            f.write(decoded_data)
            
        return f"/uploads/{filename}"
    except Exception as e:
        print(f"Error saving image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image encoding")
