import re
import requests

from .base import BaseChannel
from ..models import Video, VideoResolution, Brand


class Zdf(BaseChannel):
    BASE_API_URL = "https://api.zdf.de"

    def __init__(self):
        self.api_key = self.get_api_key()

    def get_api_key(self):
        """The API key is present in a <script> tag of the mediathek index"""
        r = requests.get("https://www.zdf.de/")
        z = re.search(r"apiToken: '(\S+)'", r.text)
        return z.group(1)

    def get_headers(self):
        return {
            "Access-Control-Request-Headers": "api-auth",
            "access-control-request-method": "GET",
            "api-auth": f"Bearer {self.api_key}",
            "host": "api.zdf.de",
            "origin": "https://www.zdf.de",
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"
        }

    def video(self, id):
        r = requests.get(f"{self.BASE_API_URL}/content/documents/ich-heisse-maja-100.json", headers=self.get_headers())
        return ZdfVideo(r.json(), channel=self, headers=self.get_headers())

    @staticmethod
    def _parse_date(date):
        return date


class ZdfVideo(Video):
    def __init__(self, data, channel, headers={}):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["leadParagraph"]
        self.appear_date = Zdf._parse_date(data["publicationDate"])
        self.expiration_date = Zdf._parse_date(data["endDate"])
        self.channel = channel
        self.brand = None

        self.headers = headers


class ZdfBrand(Brand):
    pass
