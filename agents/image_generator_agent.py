"""
agents/image_generator_agent.py

Generates distinct images from a given prompt by calling
the Hugging Face Stable Diffusion API. Each image is assigned
a unique, intelligent label based on the prompt.
"""

import requests
import base64
import random
import re
from config.settings import settings

# A simple dictionary of synonyms for intelligent label generation
SYNONYMS = {
    "horse": ["stallion", "steed", "mare"],
    "running": ["galloping", "racing", "charging"],
    "desert": ["dunes", "wasteland", "sandy expanse"],
    "sunset": ["dusk", "twilight", "evening glow"],
    "city": ["metropolis", "urban sprawl", "downtown"],
    "forest": ["woods", "grove", "jungle"]
}

# Sample style tokens for additional variety
STYLE_TOKENS = [
    "cinematic", "hyperrealistic", "watercolor", "dark-fantasy", 
    "vibrant", "minimalist", "photorealistic", "ethereal"
]

class ImageGeneratorAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key if api_key else settings.STABLE_DIFFUSION_API_KEY
        self.model_id = settings.STABLE_DIFFUSION_MODEL

    def _create_intelligent_label(self, prompt: str) -> str:
        """
        Create an intelligent label based on the prompt.
        For specific prompts like those containing "eagle" and "bird",
        select from a set of pre-defined phrases.
        Otherwise, fallback to replacing words with synonyms,
        appending a random style token, and a random 3-letter suffix.
        """
        lower_prompt = prompt.lower()
        if "eagle" in lower_prompt and "bird" in lower_prompt:
            possible_labels = [
                "eagle captured the bird",
                "bird hunted by eagle",
                "soaring eagle mid-air pursuit",
                "eagle snatches the bird",
                "bird trapped in eagle's flight"
            ]
            return random.choice(possible_labels) + "-" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=3))
        # Fallback: split prompt into words, replace with synonyms if available
        words = re.split(r"\s+", prompt.lower())
        new_words = []
        for word in words:
            clean_word = re.sub(r"[^\w]", "", word)
            if clean_word in SYNONYMS:
                new_words.append(random.choice(SYNONYMS[clean_word]))
            else:
                new_words.append(clean_word)
        base_label = "-".join(new_words)
        style = random.choice(STYLE_TOKENS)
        suffix = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=3))
        label = f"{base_label}-{style}-{suffix}"
        label = re.sub(r"-+", "-", label)
        label = re.sub(r"\d+", "", label)
        return label.strip("-")

    def generate_images(self, prompt: str, n: int = 3) -> list[dict]:
        """
        Calls the Hugging Face Stable Diffusion API to generate n images.
        Returns a list of dictionaries with keys:
          - "name": a unique, intelligent label,
          - "url": the base64-encoded image URL.
        Requests a higher resolution (768×768).
        """
        images_info = []
        for _ in range(n):
            label = self._create_intelligent_label(prompt)
            seed_value = random.randint(1, 999999)
            request_json = {
                "inputs": prompt,
                "parameters": {
                    "seed": seed_value,
                    "width": 768,
                    "height": 768
                }
            }
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.model_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=request_json,
                timeout=80
            )
            if response.status_code != 200:
                print(f"❌ Error from Hugging Face: {response.text}")
                continue
            raw_bytes = response.content
            base64_image = base64.b64encode(raw_bytes).decode("utf-8")
            data_url = f"data:image/png;base64,{base64_image}"
            images_info.append({
                "name": label,
                "url": data_url
            })
        return images_info
