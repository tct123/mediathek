import requests

from .base import BaseChannel
from ..models import Video, VideoResolution, Brand


class Zdf(BaseChannel):
    BASE_API_URL = "https://zdf-cdn.live.cellular.de/mediathekV2"

    def video(self, id):
        r = requests.get(f"{self.BASE_API_URL}/document/{id}")
        return ZdfVideo(r.json()["document"], channel=self)

    @staticmethod
    def _parse_date(date):
        return date


class ZdfVideo(Video):
    def __init__(self, data, channel):
        self.id = data["id"]
        self.title = data["titel"]
        self.description = data["beschreibung"]
        self.appear_date = Zdf._parse_date(data["date"])
        self.expiration_date = Zdf._parse_date(data["timetolive"])
        self.channel = channel
        self.brand = None
        self.download_urls = [
            VideoResolution(
                url=resolution["url"],
                resolution=resolution["quality"]
            )
            for resolution in data["formitaeten"]
        ]


class KikaBrand(Brand):
    pass
