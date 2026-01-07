from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re

load_dotenv()

class LectureMatcher:
    def __init__(self):
        print("Loading model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

    def parse_syllabus(self, syllabus_text):
        """Extract topics from syllabus text"""
        lines = syllabus_text.strip().split('/n')
        topics = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
        
            # Remove common prefixes (Week 1:, Module 2:, etc.)
            line = re.sub(r'^(Week|Module|Chapter|Lecture|Unit)\s*\d+\s*[:.-]\s*', '', line, flags=re.IGNORECASE)
            line = re.sub(r'^\d+\.\s*', '', line)  # Remove "1. "
            line = re.sub(r'^[-•]\s*', '', line)   # Remove bullets

            if len(line) > 5:
                topics.append(line)

        return topics
    
    def get_playlist_videos(self, playlist_url):
        """Fetch all videos from YouTube playlist"""
        # Extract playlist ID
        if 'list=' in playlist_url:
            playlist_id = playlist_url.split('list=')[1].split('&')[0]
        else:
            raise ValueError("Invalid playlist URL")
        
        videos = []
        next_page_token = None
        
        while True:
            request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                videos.append({
                    'title': item['snippet']['title'],
                    'video_id': item['snippet']['resourceId']['videoId'],
                    'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
                })
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos
    
    def match(self, topics, lectures, top_n=3, threshold=0.3):
        """Match topics to lectures using embeddings"""
        print(f"Mathcing {len(topics)} topics to {len(lectures)} lectures...")

        # Generate embeddings
        topic_embeddings = self.model.encode(topics)
        lecture_titles = [lec['title'] for lec in lectures]
        lecture_embeddings = self.model.encode(lecture_titles)

        results = []

        for i, topic in enumerate(topics):
            # Calculate Similarities
            similarities = cosine_similarity([topic_embeddings[i]], lecture_embeddings)[0]

            # Get Top matches above threshold
            matched_lectures = []
            for j, score in enumerate(similarities):
                if score >= threshold:
                    matched_lectures.append({
                    'lecture': lectures[i],
                    'score': float(score)
                })
                    
            matched_lectures.sort(key=lambda x: x['score'], reverse=True)
            matched_lectures = matched_lectures[:top_n]

            results.append({
                'topic': topic,
                'matches': matched_lectures
            })

        return results
    
# Main Execution
if __name__ == "__main__":
    # Initialize
    matcher = LectureMatcher()

    # sample syllabus
    syllabus = """
    Week 1: Introduction to Databases and DBMS Architecture
    Week 2: Data Models and ER Diagrams
    Week 3: Relational Model and Relational Algebra
    Week 4: SQL Basics – DDL, DML, and Constraints
    Week 5: Normalization and Functional Dependencies
    """
    playlist_url = "https://www.youtube.com/playlist?list=PLxCzCOWd7aiFAN6I8CuViBuCdJgiOkT2Y"

    # Process
    print("Parsing syllabus...")
    topics = matcher.parse_syllabus(syllabus)
    print(f"Found {len(topics)} topics\n")

    print("Fetching playlist...")
    lectures = matcher.get_playlist_videos(playlist_url)
    print(f"Found {len(lectures)} lectures\n")
    
    print("Matching...")
    results = matcher.match(topics, lectures)

    # Display results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80 + "\n")
    
    for result in results:
        print(f"📚 {result['topic']}")
        if result['matches']:
            for match in result['matches']:
                print(f"   → {match['lecture']['title']}")
                print(f"      Score: {match['score']:.2f} | {match['lecture']['url']}")
        else:
            print("   → No matches found")
        print()






