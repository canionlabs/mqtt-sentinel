from .services import DB_LIST


class DBManager:
    DATABASE_SERVICES = DB_LIST

    def __init__(self, url, external_service=None):
        self.url = url
        self.db = external_service or self.select_database()

    def select_database(self):
        for avaliable_database in self.DATABASE_SERVICES:
            if avaliable_database.check_url(self.url):
                return avaliable_database

    def get_topics(self):
        return self.db.get_topics()
