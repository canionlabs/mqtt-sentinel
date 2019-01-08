from .base import BaseService
from sentinel.rules import RuleDBObject

from functools import wraps
import sqlite3


def sqlite_action(action):
    @wraps(action)
    def _mod(self, *method_args, **method_kwargs):
        self._open()
        value_return = action(self, *method_args, **method_kwargs)
        self._commit()
        return value_return
    return _mod


class SQLite3(BaseService):
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
        self.cursor.execute(f"""
            INSERT INTO rules (
                topic, operator, equated
            ) VALUES (
                "{rule.topic}", "{rule.operator}", "{rule.equated}"
            )
        """)

    @sqlite_action
    def get_rules(self):
        rules = []
        query = self.cursor.execute("""
            SELECT topic, operator, equated FROM rules;
        """)
        results = query.fetchall()
        for result in results:
            rules.append(RuleDBObject(*result))
        return rules

    def __call__(self, database):
        self._set_db(database)

    @staticmethod
    def _set_db(db):
        return db[9:]

    @classmethod
    def _check_url(cls, url):
        return url.startswith('sqlite://')
