from fastapi import APIRouter, File, UploadFile
from services.s3 import upload_to_s3

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    url = upload_to_s3(file)
    return {"image_url": url}