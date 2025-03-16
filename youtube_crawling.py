import requests
import re
import pandas as pd
from googleapiclient.discovery import build

class YoutubeCrawling:
    def __init__(self, api_key: str):
        """Inisialisasi YouTube API."""
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def extract_video_id(self, url: str) -> str:
        """Mengekstrak video ID dari URL YouTube."""
        match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
        return match.group(1) if match else None

    def get_comments(self, video_url: str, max_comments: int = 100, order="relevance"):
        """Mengambil komentar dari video YouTube."""
        video_id = self.extract_video_id(video_url)
        if not video_id:
            raise ValueError("URL YouTube tidak valid.")

        comments = []
        next_page_token = None

        while len(comments) < max_comments:
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=min(100, max_comments - len(comments)),
                order=order,
                pageToken=next_page_token
            ).execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break  # Hentikan jika tidak ada komentar lagi

        return comments


# YouTube Data API key (Gantilah dengan API key Anda)
API_KEY = 'AIzaSyCwGg_Quc1Ie99GeTvaoF_BHpqWcj0sdDc'

# API Endpoint
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

# # VIDEO_ID YOUTUBE
# VIDEO_ID = 'Q01bKunF76g'
# COMMENT_LIMIT = 100  # Jumlah komentar yang ingin diunduh

def get_comments(video_id, api_key, max_results=100):
    comments = []
    next_page_token = None

    while len(comments) < max_results:
        params = {
            'part': 'snippet',
            'videoId': video_id,
            'key': api_key,
            'maxResults': min(100, max_results - len(comments)),
            'textFormat': 'plainText',
            'pageToken': next_page_token if next_page_token else ''
        }

        response = requests.get(YOUTUBE_API_URL, params=params)
        data = response.json()

        if 'items' not in data:
            print("Error fetching comments:", data)
            break

        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'comment': comment['textDisplay'],
                'likes': comment['likeCount'],
                'published_at': comment['publishedAt']
            })

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return comments

def main_crawling(idVideo, limmitComment):
    
    # Mendapatkan komentar
    comments_data = get_comments(idVideo, API_KEY, limmitComment)

    # Simpan ke CSV
    if comments_data:
        df = pd.DataFrame(comments_data)
        df.to_csv('ytb_comments.csv', index=False)
        print("Komentar berhasil disimpan dalam ytb_comments.csv")
    else:
        print("Tidak ada komentar yang diunduh.")

