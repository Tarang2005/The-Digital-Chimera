from io import BytesIO
from PIL import Image
import boto3
import requests
from app.core.config import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    endpoint_url=settings.AWS_ENDPOINT_URL
)

def upload_to_s3(file_bytes: bytes, filename: str) -> str:
    s3_client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=filename,
        Body=file_bytes,
        ContentType='image/png',
        ACL='public-read'
    )
    return f"{settings.AWS_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{filename}"

def stitch_images(head_url: str, torso_url: str, legs_url: str) -> bytes:
    head_response = requests.get(head_url)
    torso_response = requests.get(torso_url)
    legs_response = requests.get(legs_url)

    head_img = Image.open(BytesIO(head_response.content)).convert("RGBA")
    torso_img = Image.open(BytesIO(torso_response.content)).convert("RGBA")
    legs_img = Image.open(BytesIO(legs_response.content)).convert("RGBA")

    # Assuming 500x500 each segment
    final_img = Image.new("RGBA", (500, 1500))
    final_img.paste(head_img, (0, 0))
    final_img.paste(torso_img, (0, 500))
    final_img.paste(legs_img, (0, 1000))

    img_byte_arr = BytesIO()
    final_img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def get_connection_sliver(image_url: str, height: int = 20) -> bytes:
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    width, original_height = img.size
    
    # Crop the bottom `height` pixels
    sliver = img.crop((0, original_height - height, width, original_height))
    
    img_byte_arr = BytesIO()
    sliver.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
