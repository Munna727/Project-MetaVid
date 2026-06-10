import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("CLOUDINARY_API_KEY"))

# Configure once (on app startup)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def cloudinary_upload(file_path):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

    result = cloudinary.uploader.upload(
        file_path,
        resource_type="video",        # MUST be video
        folder="metavid/results",
        overwrite=True
    )

    return result["secure_url"]
