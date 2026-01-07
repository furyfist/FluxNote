from flask import Flask, request, jsonify
from flask_cors import CORS
from matcher import LectureMatcher

app = Flask(__name__)
CORS(app)

# Initialize matcher once
matcher = LectureMatcher()

@app.route('/api/match', methods=['POST'])
def match_lectures():
    try:
        data = request.json
        playlist_url = data.get('playlist_url')
        syllabus_text = data.get('syllabus')

        if not playlist_url or not syllabus_text:
            return jsonify({'error': 'Missing Playlist_url or Syllabus'}), 400
        
        # Process
        topics = matcher.parse_syllabus(syllabus_text)
        lectures = matcher.get_playlist_videos(playlist_url)
        results = matcher.match(topics, lectures)

        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/match', methods=['GET'])
def test_match():
    """Test endpoint - remove in production"""
    return jsonify({
        'message': 'API is working! Send a POST request with playlist_url and syllabus',
        'example': {
            'playlist_url': 'https://youtube.com/playlist?list=...',
            'syllabus': 'Topic 1\nTopic 2\nTopic 3'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
