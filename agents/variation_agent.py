"""
agents/variation_agent.py

Creates variations of a prompt.
Then calls ImageGeneratorAgent to get images for each variation.
"""

import random
from agents.image_generator_agent import ImageGeneratorAgent

class VariationAgent:
    def __init__(self):
        # If needed, pass keys or settings here
        self.generator = ImageGeneratorAgent()

    def create_variations(self, original_prompt: str, num_variations: int = 3) -> list[str]:
        """
        Simple placeholder approach:
        1. Splits words,
        2. Randomly appends or replaces words with style tokens or synonyms.

        In real usage, you might call an LLM or have style libraries.
        """
        # Example style tokens
        style_tokens = ["--style watercolor", "--style abstract", "--style realism", "--style fantasy"]

        variations = []
        for i in range(num_variations):
            # For demonstration, we simply append a random style token to the prompt
            style = random.choice(style_tokens)
            new_prompt = f"{original_prompt} {style}"
            variations.append(new_prompt.strip())
        return variations

    def generate_variation_images(self, original_prompt: str, num_variations: int = 3) -> dict:
        """
        1. Create prompt variations
        2. Use ImageGeneratorAgent to produce images for each variation
        3. Return a dict: { variation_prompt: [imageURLs], ... }
        """
        variation_prompts = self.create_variations(original_prompt, num_variations)
        results = {}

        for prompt in variation_prompts:
            images = self.generator.generate_images(prompt, n=1)
            results[prompt] = images

        return results
