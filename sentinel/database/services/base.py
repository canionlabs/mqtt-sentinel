class BaseService:

    @classmethod
    def _check_url(cls, url):
        raise NotImplementedError()

    @classmethod
    def check_url(cls, url):
        return cls._check_url(url)
