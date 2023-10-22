from src.channel import Channel
import datetime
import isodate


class PlayList(Channel):
    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.info = Channel.get_service().playlists().list(id=self.id_playlist,
                                                           part='snippet,contentDetails',
                                                           maxResults=50).execute()
        self.title = self.info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.id_playlist}"
        self.playlist_videos = Channel.get_service().playlistItems().list(playlistId=self.id_playlist,
                                                                          part='contentDetails',
                                                                          maxResults=50).execute()

        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

    @property
    def total_duration(self):
        time_list = []
        video_response = Channel.get_service().videos().list(part='contentDetails,statistics',
                                                             id=','.join(self.video_ids)).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_list.append(duration.total_seconds())

        hours = sum(time_list) // 3600
        minutes = (sum(time_list) - hours * 3600) // 60
        seconds = sum(time_list) % 60
        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def show_best_video(self):
        like_dict = {}
        for video in self.video_ids:
            video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video).execute()
            like_count = video_response['items'][0]['statistics']['likeCount']
            like_dict[like_count] = f'https://youtu.be/{video}'
        return like_dict[max(like_dict.keys())]
