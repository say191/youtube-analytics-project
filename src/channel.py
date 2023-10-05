import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    apikey = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=apikey)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.info = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.info, indent=2, ensure_ascii=False))
