import requests
from datetime import datetime

from .base import BaseChannel
from ..models import Video, VideoResolution


class Kika(BaseChannel):
    BASE_API_URL = "https://prod.kinderplayer.cdn.tvnext.tv/api"

    def all_videos(self):
        r = requests.get(f"{self.BASE_API_URL}/videos")
        videos = r.json()["_embedded"]["items"]
        results = []

        for video_data in videos:
            results.append(KikaVideo(video_data))

        return

    def video(self, id):
        r = requests.get(f"{self.BASE_API_URL}/videos/{id}")
        return KikaVideo(r.json())

    @staticmethod
    def _parse_date(raw_date):
        return datetime.now()


class KikaVideo(Video):
    def __init__(self, data):
        self.channel = self
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.appear_date = Kika._parse_date(data["appearDate"])
        self.expiration_date = Kika._parse_date(data["expirationDate"])

    def download_urls(self):
        r = requests.get(f"{Kika.BASE_API_URL}/videos/{self.id}/player-assets")
        results = []

        for resolution in r.json()["hbbtvAssets"]:
            results.append(
                VideoResolution(
                    url=resolution["url"],
                    resolution=resolution["quality"].split(" | ")[-1]
                )
            )

        return results
