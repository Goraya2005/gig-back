import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    STABLE_DIFFUSION_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    STABLE_DIFFUSION_MODEL = os.getenv("HUGGINGFACE_MODEL", "")
    # If you have supabase or other keys, keep them as is
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

settings = Settings()
