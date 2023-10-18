import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, id_video: str):
        self.id_video = id_video
        self.video_response = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                id=self.id_video).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url: str = f"https://youtu.be/{self.id_video}"
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        apikey = os.getenv('API_KEY')
        return build('youtube', 'v3', developerKey=apikey)


class PLVideo(Video):
    def __init__(self, id_video: str, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
        self.video_response = Video.get_service().playlistItems().list(playlistId=self.id_playlist,
                                                                       part='contentDetails',
                                                                       maxResults=50).execute()
