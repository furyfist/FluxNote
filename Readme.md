# FluxNote

**FluxNote** is an intelligent lecture-to-syllabus matching system that helps students and educators efficiently map YouTube playlist lectures to their course syllabus topics using AI-powered semantic similarity.

## 🚀 Features

- **Smart Topic Matching**: Uses sentence transformers and cosine similarity to match syllabus topics with YouTube lecture titles
- **YouTube Integration**: Automatically fetches all videos from YouTube playlists
- **Flexible Syllabus Parsing**: Intelligently extracts topics from various syllabus formats
- **REST API**: Flask-based backend API for easy integration
- **Modern Frontend**: React + TypeScript frontend for a seamless user experience
- **Document Parser**: Supports multiple file formats (TXT, DOCX, PDF, Images) for syllabus extraction

## 📁 Project Structure

```
FluxNote/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── styles/          # CSS styling
│   └── package.json
├── fluxnote-parser/         # Document parsing module
│   ├── parsers/             # File format parsers
│   └── utils/               # Utility functions
├── app.py                   # Flask API server
├── matcher.py               # Core matching algorithm
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## 🛠️ Tech Stack

### Backend
- **Python 3.x**
- **Flask** - Web framework
- **Sentence Transformers** - Semantic embeddings
- **scikit-learn** - Cosine similarity calculations
- **Google YouTube API** - Playlist data fetching
- **python-dotenv** - Environment management

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **React Scripts** - Build tooling

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials))

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FluxNote
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the root directory:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

#### Start the Flask Server

```bash
python app.py
```

The API server will start on `http://localhost:5000`

### 3. Frontend Setup

#### Navigate to Frontend Directory

```bash
cd frontend
```

#### Install Dependencies

```bash
npm install
```

#### Start Development Server

```bash
npm start
```

The frontend will open at `http://localhost:3000`

## 🎯 Usage

### Using the API

#### Health Check
```bash
GET http://localhost:5000/api/health
```

#### Match Lectures to Syllabus
```bash
POST http://localhost:5000/api/match
Content-Type: application/json

{
  "playlist_url": "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID",
  "syllabus": "Week 1: Introduction to Databases\nWeek 2: Data Models\nWeek 3: SQL Basics"
}
```

#### Response Format
```json
{
  "success": true,
  "results": [
    {
      "topic": "Introduction to Databases",
      "matches": [
        {
          "lecture": {
            "title": "Database Fundamentals",
            "video_id": "abc123",
            "url": "https://www.youtube.com/watch?v=abc123"
          },
          "score": 0.85
        }
      ]
    }
  ]
}
```

### Using the Python Module Directly

```python
from matcher import LectureMatcher

# Initialize matcher
matcher = LectureMatcher()

# Parse syllabus
syllabus_text = """
Week 1: Introduction to Databases
Week 2: Data Models and ER Diagrams
Week 3: SQL Basics
"""
topics = matcher.parse_syllabus(syllabus_text)

# Fetch playlist videos
playlist_url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
lectures = matcher.get_playlist_videos(playlist_url)

# Match topics to lectures
results = matcher.match(topics, lectures, top_n=10, threshold=0.3)
```

## ⚙️ Configuration

### Matching Parameters

- **top_n**: Maximum number of matches per topic (default: 10)
- **threshold**: Minimum similarity score (0-1) to consider a match (default: 0.3)

### Syllabus Format Support

The parser automatically handles various syllabus formats:
- Week-based: `Week 1: Topic Name`
- Module-based: `Module 2: Topic Name`
- Numbered: `1. Topic Name`
- Bullet points: `- Topic Name` or `• Topic Name`

## 🧪 Testing

### Run Matcher Tests
```bash
python test_matcher.py
```

### Run YouTube API Tests
```bash
python youtube_test.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

The production build will be created in the `frontend/build` directory.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Common Issues

**YouTube API Quota Exceeded**
- The YouTube API has daily quota limits. If exceeded, wait 24 hours or use a different API key.

**Model Loading Errors**
- Ensure you have sufficient disk space for the sentence transformer model (~80MB)
- Check your internet connection for first-time model download

**CORS Errors**
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that the frontend is making requests to the correct backend URL

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Made with ❤️ for students and educators**
