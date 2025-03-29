from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from routes.image_routes import router as image_router

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Image Generator - Backend")

# Enable CORS so the frontend on a different domain can call the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your actual domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include image-related routes.
app.include_router(image_router, prefix="/api")

# Global exception handler to log unexpected errors.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": str(exc)},
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
