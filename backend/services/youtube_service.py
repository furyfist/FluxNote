from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Optional
import os
import re
from models.schemas import YouTubeVideo

class YouTubeService:
    """
    Handles all Youtube Api Interactions
    """

    def __init__(self):
        """
        Initialize Youtube API Client

        Args: 
            api_key : Youtube Data API v3 key (loads from env)
        """
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found")

        self.youtube = build('youtube', 'v3', developerKey = self.api_key)
    
    def extract_playlist_id(self, playlist_url: str) -> str:
        """
        Extract playlist ID from various Youtube URL formats

        Supports:
        -  https://www.youtube.com/playlist?list=PLxxx
        - https://youtube.com/playlist?list=PLxxx
        - https://www.youtube.com/watch?v=xxx&list=PLxxx

        Args:
            playlist_url: Youtube Playlist URL

        Returns: 
            playlist ID String

        Raises:
            ValueError: If URL format is inValid
        """

        # pattern to match list parameter
        pattern = r'[?&]list=([a-zA-Z0-9_-]+)'
        match = re.search(pattern, playlist_url)

        if not match:
            raise ValueError(
                "Invalid playlist URL. Must contain 'list=' parameter. "
                "Example: https://www.youtube.com/playlist?list=PLxxx"
            )

        playlist_id = match.group(1)

        # validate playlist ID format (starts with PL, UU, etc.)
        if not re.match(r'^[A-Z]{2}[a-zA-Z0-9_-]{16,}$', playlist_id):
            raise ValueError(f"Invalid Playlist ID Format: {playlist_id}")

        return playlist_id

    def fetch_playlist_videos(self, playlist_url: str) -> List[YouTubeVideo] :
        """
        Fetch all videos from a Youtube Playlist

        Args: 
            playlist_url: Youtube playlist URL

        Returns:
            List of YoutubeVideo objects with title, url, position

        Raises:
            ValusError: If playlist URL is invaid
            HttpError: If Youtube API request fails
        """

        playlist_id = self.extract_playlist_id(playlist_url)

        videos = []
        next_page_token = None
        position = 1

        try:
            while True:
                # API request
                request = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken= next_page_token
                )

                response = request.execute()

                # Parse videos
                for item in response['items']:
                    snippet = item['snippet']

                    # Skip deleted/private Videos
                    if snippet['title'] == 'Deleted video' or snippet['title'] == 'Private video':
                        continue

                    video_id = snippet['resourceId']['videoId']

                    videos.append(YouTubeVideo(
                        title=snippet['title'],
                        video_id=video_id,
                        url= f"https://www.youtube.com/watch?v={video_id}",
                        position = position
                    ))

                    position += 1

                # Check for next Page
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
            return videos

        except HttpError as e:
            if e.resp.status == 404:
                raise ValueError(f"Playlist not found: {playlist_id}")
            elif e.resp.status == 403:
                raise ValueError("YouTube API quota exceeded or invalid API key")
            else:
                raise ValueError(f"YouTube API error: {str(e)}")

    def get_video_count(self, playlist_url: str) -> int:
        """
        Get total number of videos in playlist (quick check)

        Args:
            playlist_Url : Youtube Playlist URL

        Returns:
            Total Video count
        """

        playlist_id = self.extract_playlist_id(playlist_url)

        try:
            request = self. extract_playlist().list(
                part = 'contentDetails',
                id = playlist_id
            )
            response = request.execute()

            if not response['items']:
                return 0

            return response['items'][0]['contentDetails']['itemCount']

        except HttpError:
            return 0



    




