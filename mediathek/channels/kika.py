import requests
from datetime import datetime

from .base import BaseChannel
from ..models import Video


class Kika(BaseChannel):
    BASE_API_URL = "https://prod.kinderplayer.cdn.tvnext.tv/api/"

    def all_videos(self):
        r = requests.get(self.BASE_API_URL + "videos")
        videos = r.json()["_embedded"]["items"]
        results = []

        for video in videos:
            results.append(self._parse_video(video))

        return

    def video(self, id):
        r = requests.get(self.BASE_API_URL + "videos/" + id)
        return self._parse_video(r.json())

    def _parse_video(self, data):
        return Video(
            channel=self,
            id=data["id"],
            title=data["title"],
            description=data["description"],
            appear_date=self._parse_date(data["appearDate"]),
            expiration_date=self._parse_date(data["expirationDate"])
        )

    def _parse_date(self, raw_date):
        return datetime.now()
