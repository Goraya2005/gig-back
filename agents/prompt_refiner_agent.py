# agents/prompt_refiner_agent.py

from langchain import PromptTemplate, LLMChain
from config.settings import settings
from langchain_google_genai import GoogleGenerativeAI

class PromptRefinerAgent:
    def __init__(self, api_key: str = None):
        # Use the provided key or fallback to GOOGLE_API_KEY from settings.
        self.api_key = api_key if api_key else settings.GOOGLE_API_KEY
        
        # Initialize the Gemini LLM using GoogleGenerativeAI.
        # Ensure you have the correct model name ("gemini-2.0-flash-exp" is assumed).
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=self.api_key)
        
        # Define a prompt template for refining the creative prompt.
        self.template = PromptTemplate(
            input_variables=["prompt"],
            template="Refine the following creative prompt for generating high-quality images: {prompt}"
        )
        
        # Create an LLMChain using the Gemini LLM.
        self.chain = LLMChain(llm=self.llm, prompt=self.template)

    def refine_prompt(self, raw_prompt: str) -> str:
        refined = self.chain.run({"prompt": raw_prompt})
        return refined.strip()
