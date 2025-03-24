from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.image_routes import router as image_router

app = FastAPI(title="AI Image Generator - Backend")

# 1) Enable CORS so Vercel (a different domain) can call your Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # For production, specify your actual domain(s) for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
