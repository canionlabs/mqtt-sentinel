# coding: utf-8
from sentinel.database import manager


class Sentinel:
    def __init__(self):
        self.db_url = None
        self.db = None

    def db_config(self, db_url):
        self.set_db(db_url)

    def set_db(self, db_url):
        self.db = manager(db_url)
        self.db_url = db_url
        self.db.migrate()
