from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

def get_playlist_videos(playlist_url):
    # Extract Playlist ID
    if 'list=' in playlist_url:
        playlist_id = playlist_url.split('list=')[1].split('&')[0]
    else:
        print("Invalid Playlist URL")
        return []
    
    # Initialize Youtube API
    youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

    videos = []
    next_page_token = None

    while True:
        # Fetch Playlist items
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId = playlist_id,
            maxResults = 1000,
            pageToken = next_page_token
        )
        response = request.execute()

        # Extract Video info
        for item in response['items']:
            videos.append({
                'title': item['snippet']['title'],
                'video_id': item['snippet']['resourceId']['videoId'],
                'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            })

        # checking if there are more pages
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

# Test with a real playlist
playlist_url = "https://www.youtube.com/playlist?list=PLxCzCOWd7aiFAN6I8CuViBuCdJgiOkT2Y"

videos = get_playlist_videos(playlist_url)
print(f"Found {len(videos)} videos:\n")
for i,video in enumerate(videos[:5], 1):
    print(f"{i}. {video['title']}")
    print(f" {video['url']}\n")