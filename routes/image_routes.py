# routes/image_routes.py


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.image_generator_agent import ImageGeneratorAgent

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str
    num_images: int = 3  # Generate three images by default

@router.post("https://gig-back.onrender.com/api/generate-image")
def generate_image(request: ImageRequest):
    try:
        generator = ImageGeneratorAgent()
        images_info = generator.generate_images(request.prompt, n=request.num_images)
        if not images_info:
            raise HTTPException(status_code=500, detail="No images generated")
        return {"images": images_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
