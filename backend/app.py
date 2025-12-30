from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config import settings
from auth.routes import router as auth_router
from api.routes import router as api_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Resona API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(api_router)

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "spotify_configured": bool(settings.spotify_client_id and settings.spotify_client_secret),
        "jwt_configured": bool(settings.jwt_secret),
        "database": "sqlite",
        "endpoints": {
            "auth_login": "/auth/login",
            "auth_callback": "/auth/callback",
            "auth_me": "/auth/me",
            "api_profile": "/api/profile",
            "api_profile_summary": "/api/profile/summary",
            "api_features": "/api/features"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
