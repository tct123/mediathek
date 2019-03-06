class Video:
    def __init__(self, channel, id, title, description, appear_date, expiration_date):
        self.channel = channel
        self.id = id
        self.title = title
        self.description = description
        self.appear_date = appear_date
        self.expiration_date = expiration_date


class VideoResolution:
    def __init__(self, url, resolution):
        self.url = url
        self.resolution = resolution
