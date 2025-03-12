"""
routes/variation_routes.py

Handles requests to create and generate variations of a given prompt.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.variation_agent import VariationAgent

router = APIRouter()

class VariationRequest(BaseModel):
    prompt: str
    num_variations: int = 3

@router.post("/generate-variations")
def generate_variations(request: VariationRequest):
    try:
        variation_agent = VariationAgent()
        # This method will both create new variation prompts 
        # and generate images for each variation
        variation_results = variation_agent.generate_variation_images(
            original_prompt=request.prompt,
            num_variations=request.num_variations
        )
        """
        variation_results is a dict like:
        {
          "horse running in desert --style abstract": ["data:image/png;base64,..."],
          "horse running in desert --style realism": ["data:image/png;base64,..."],
          ...
        }
        """
        if not variation_results:
            raise HTTPException(status_code=500, detail="No variations generated")

        return {"variations": variation_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
