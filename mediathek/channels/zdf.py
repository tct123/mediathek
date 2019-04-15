import requests

from .base import BaseChannel
from ..models import Video, Brand


class Zdf(BaseChannel):
    BASE_API_URL = "https://zdf-cdn.live.cellular.de/mediathekV2"

    def video(self, id):
        r = requests.get(f"{self.BASE_API_URL}/document/{id}")
        return ZdfVideo(r.json()["document"], channel=self)


class ZdfVideo(Video):
    def __init__(self, data, channel):
        self.id = data["id"]


class KikaBrand(Brand):
    pass
