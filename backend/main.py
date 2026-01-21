from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from typing import Dict

# Import our services and models
from services.youtube_service import YouTubeService
from services.ai_service import AIMatchingService
from models.schemas import(
    MatchRequest,
    MatchResponse,
    ErrorResponse,
    TopicMatch
)

load_dotenv()

# Initialize 
app = FastAPI(
    title="FluxNote",
    description="AI-powered syllabus to Youtube lecture matching service",
    version="1.0.0"
)

# CORS middleware - allows frontend to call this app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # when deploy, change this to fronend url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services globally
youtube_service = YouTubeService()
ai_service = AIMatchingService()


# API ENDPOINTS

@app.get("/")
async def root():
    """Health Check endpoint"""
    return {
        "status" : "online",
        "message" : "Lecture Matcher API is running",
        "Version": "1.0.0"
    }
@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status" : "online",
        "services": {
            "youtube": "configured" if os.getenv('YOUTUBE_API_KEY') else "missing youtube API Key",
            "gemini" : "configured" if os.getenv('GEMINI_API_KEY') else "missing gemini API key"
        }
    }

@app.post("/api/match", response_model = MatchResponse)
async def match_lectures(request: MatchRequest):
    """
    Main endpoint: Match syllabus topics to YouTube lectures

    Args:
        request: MatchRequest with syllabus_text and playlist_url

    Returns:
        MatchResponse with matched lectures
    
    Raises:
        HTTPExecution: If any step fails
    """
    try:
        # Fetch youtube playlist videos
        print(f"Fetching Playlist: {request.playlist_url}")
        lectures = youtube_service.fetch_playlist_videos(str(request.playlist_url))

        if not lectures:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Videos found in playlist or playlist is empty"
            )
        print(f"Found {len(lectures)} lectures")

        # AI Matching with Gemini
        print(f"Matching with AI...")
        matches = ai_service.matched_lectures(request.syllabus_text, lectures)
        print(f"Matched {len(matches)} topics")

        # Build Response
        response = MatchResponse(
            success=True,
            total_topics=len(matches),
            total_lectures_fetched=len(lectures),
            matches=matches,
            message=f"Successfully matched {len(matches)} topics to {len(lectures)} lectures"
        )
        return response

    except ValueError as e:
        # Handle validation errors(bad Urls, empty inputs, etc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Handle unexpected errors
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

@app.post("/api/validate-playlist")
async def validate_playlist(data: Dict[str, str]):
    """
    Quick endpoint to validate a playlist URL without full matching

    Args:
        data: Dictionary with 'playlist_url' key

    Returns:
        Video count and basic info
    """

    try:
        playlist_url = data.get('playlist_url')
        if not playlist_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="playlist_url is required"
            )

        # Extract and validate playlist ID
        playlist_id = youtube_service.extract_playlist_id(str(playlist_url))

        # Get Video count
        video_count = youtube_service.get_video_count(str(playlist_url))

        return {
            "valid": True,
            "playlist_id": playlist_id,
            "video_count": video_count,
            "message": f"Found {video_count} videos in playlist"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Catch-all exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "An unexpected error occurred",
            "details": str(exc)
        }
    )

# Startup Event

@app.on_event("startup")
async def startup_event():
    """Run on server startup"""
    print("fluxnote starting :)")

    # Check API Keys
    youtube_key = os.getenv('YOUTUBE_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')

    if not youtube_key:
        print("WARNING: YOUTUBE_API_KEY not found in environment")
    else:
        print("YouTube API configured")
    
    if not gemini_key:
        print("WARNING: GEMINI_API_KEY not found in environment")
    else:
        print("Gemini API configured")

    print("API docs at http://localhost:8000/docs")

# Run Server 

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main: app",
        host="0.0.0.0",
        port=8000,
        reload=True, # Auto-reload on code changes
        log_level="info"
    ) 