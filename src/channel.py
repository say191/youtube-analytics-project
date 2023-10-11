import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.info = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.info['items'][0]['snippet']['title']
        self.description = self.info['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.info['items'][0]['id']}"
        self.subs_count = int(self.info['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.info['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.info['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subs_count+other.subs_count

    def __sub__(self, other):
        return self.subs_count-other.subs_count

    def __gt__(self, other):
        return self.subs_count>other.subs_count

    def __ge__(self, other):
        return self.subs_count>=other.subs_count

    def __lt__(self, other):
        return self.subs_count<other.subs_count

    def __le__(self, other):
        return self.subs_count<=other.subs_count

    def __eq__(self, other):
        return self.subs_count==other.subs_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.info, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        apikey = os.getenv('API_KEY')
        return build('youtube', 'v3', developerKey=apikey)

    def to_json(self, name_file: str):
        data = {'channel_id': self.__channel_id, 'title': self.title, 'description': self.description,
                'url': self.url, 'subs_count': self.subs_count, 'video_count': self.video_count,
                'view_count': self.view_count}
        with open(name_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
