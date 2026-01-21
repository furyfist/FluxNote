from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

# Request Models 
class MatchRequest(BaseModel):
    """
    Request payload for mathching syllabus to lectures (frontend sends)
    """
    syllabus_text: str = Field(
        ...,
        min_length = 10,
        max_length = 5000,
        description = "Full syllabus text containing topics/modules"
    )
    playlist_url: HttpUrl = Field(
        ...,
        description="Youtube Playlist URL (must be public)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "syllabus_text": "Week 1: Intro to DB\nWeek 2: SQL Basics",
                "playlist_url": "https://www.youtube.com/playlist?list=PLxxx"
            }
        }

# Response Models
class MatchedLecture(BaseModel):
    """
    Single matched lecture with metadata
    """
    title: str = Field(..., description="Lecture title")
    url: HttpUrl = Field(..., description = "Youtube video URL")
    reasoning: str = Field(..., description = "Why this lecture matches the topic")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Mathch confidence score")
    order: int = Field(..., ge=1, description="Recommended watch order")

class TopicMatch(BaseModel):
    """
    A syllabus topic with its matched lectures
    """
    topic: str = Field(..., description="Original syllabus topic text")
    matched_lectures: List[MatchedLecture] = Field(
        default_factory= list,
        description="List of relevent lectures for this topic"
    )

class MathchResponse(BaseModel):
    """
    Complete response with all features
    """
    success : bool = Field(default=True)
    total_topics: int = Field(..., description="Number of syllabus topics processed")
    total_lectures_fetched: int = Field(..., description="Total videos in playlist")
    matches: List[TopicMatch] = Field(..., description="Mathced topics and lectures")
    message: Optinal[str] = Field(None, description="Additional message or info")

# Youtube Service Models

class YoutubeVideo(BaseModel):
    """
    Youtube Video Metadata
    """
    titlle: str
    video: str
    url: HttpUrl
    position: int = Field(..., description="Video position in playlist (1-indexed)")

# Error Response Models

class ErrorResponse(BaseModel):
    """
    Standard Error response  
    """
    success: bool = Field(default=False)
    message: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional details")




