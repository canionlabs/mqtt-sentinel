from .base import BaseService


class PostgresService(BaseService):
    def __init__(self, url):
        self.url = url

    @classmethod
    def _check_url(cls, url):
        return url.startswith('postgres://')
