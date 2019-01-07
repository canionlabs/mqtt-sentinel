from .base import BaseService

from functools import wraps
import sqlite3


def sqlite_action(action):
    @wraps(action)
    def _mod(self, *method_args, **method_kwargs):
        self._open()
        action(self, *method_args, **method_kwargs)
        self._commit()
    return _mod


class SQlite3(BaseService):
    def __init__(self, database):
        self.database = self._set_db(database)
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect(self.database)

    def _open(self):
        self.cursor = self.conn.cursor()

    def _commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    @sqlite_action
    def migrate(self):
        try:
            self.cursor.execute("""
                CREATE TABLE rules (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    operator TEXT NOT NULL,
                    equated TEXT NULL
                );
            """)
        except sqlite3.OperationalError as e:
            # print error log
            print(e)

    @sqlite_action
    def add_rule(self, rule):
        import pdb; pdb.set_trace
        self.cursor.execute(f"""
            INSERT INTO rules (
                topic, operator, equated
            ) VALUES (
                "{rule.topic}", "{rule.operator}", "{rule.equated}"
            )
        """)

    def __call__(self, database):
        self._set_db(database)

    @staticmethod
    def _set_db(db):
        return db[9:]

    @classmethod
    def _check_url(cls, url):
        return url.startswith('sqlite://')
