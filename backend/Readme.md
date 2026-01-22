# Backend Flow

User Input (Frontend)
    ↓
[Syllabus Text + Playlist URL]
    ↓
FastAPI Backend
    ↓
YouTube Service → Fetch all video titles
    ↓
AI Service → Claude API
    ↓
Prompt: "Match these topics to lectures in order"
    ↓
Claude Response (Structured JSON)
    ↓
Backend formats response
    ↓
Frontend displays results