# Lecture Matcher Frontend

A modern React frontend application for matching YouTube playlist lectures with syllabus topics.

## Features

- 🎯 **Smart Matching**: Match YouTube lectures with your syllabus topics using AI
- 🎨 **Modern UI**: Clean, professional design with blue/green theme
- 📱 **Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- ⚡ **Real-time Validation**: Instant form validation with helpful error messages
- 🔍 **Score-based Results**: Color-coded similarity scores for easy interpretation
- 🎓 **YouTube Integration**: Direct links to matched lectures

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Form/
│   │   │   ├── MatchForm.jsx       # Main form component
│   │   │   └── MatchForm.css
│   │   ├── Results/
│   │   │   ├── ResultsDisplay.jsx  # Results container
│   │   │   ├── TopicSection.jsx    # Individual topic section
│   │   │   ├── LectureCard.jsx     # Lecture card with link
│   │   │   └── Results.css
│   │   ├── UI/
│   │   │   ├── LoadingSpinner.jsx  # Loading state
│   │   │   ├── ErrorMessage.jsx    # Error display
│   │   │   ├── ScoreBadge.jsx      # Score badge
│   │   │   └── UI.css
│   │   └── Layout/
│   │       ├── Header.jsx          # App header
│   │       ├── Footer.jsx          # App footer
│   │       └── Layout.css
│   ├── services/
│   │   └── api.js                  # API service layer
│   ├── utils/
│   │   └── validation.js           # Validation utilities
│   ├── styles/
│   │   ├── variables.css           # CSS variables
│   │   ├── global.css              # Global styles
│   │   └── theme.css               # Theme styles
│   ├── App.jsx                     # Main app component
│   ├── App.css
│   └── index.js                    # Entry point
├── package.json
└── README.md
```

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Development

1. **Start the development server:**
   ```bash
   npm start
   ```

2. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

3. **Ensure backend is running:**
   The backend API should be running on [http://localhost:5000](http://localhost:5000)

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## API Integration

The frontend connects to the backend API at `http://localhost:5000/api/match`

**Request Format:**
```json
{
  "playlist_url": "https://www.youtube.com/playlist?list=...",
  "syllabus": "Topic 1\nTopic 2\nTopic 3"
}
```

**Response Format:**
```json
{
  "success": true,
  "results": [
    {
      "topic": "Introduction to Databases",
      "matches": [
        {
          "lecture": {
            "title": "Lecture 1: Database Basics",
            "video_id": "abc123",
            "url": "https://www.youtube.com/watch?v=abc123"
          },
          "score": 0.87
        }
      ]
    }
  ]
}
```

## Component Documentation

### Form Component (`MatchForm`)
- Handles user input for playlist URL and syllabus
- Validates input before submission
- Shows loading state during API calls

### Results Components
- **ResultsDisplay**: Container for all results
- **TopicSection**: Groups lectures by topic
- **LectureCard**: Individual lecture with YouTube link and score

### UI Components
- **LoadingSpinner**: Animated loading indicator
- **ErrorMessage**: Error display with retry option
- **ScoreBadge**: Color-coded score display (green/yellow/gray)

## Styling

The application uses a custom CSS design system with:
- CSS variables for consistent theming
- Blue/green gradient color scheme
- Responsive breakpoints for mobile/tablet/desktop
- Smooth transitions and animations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
