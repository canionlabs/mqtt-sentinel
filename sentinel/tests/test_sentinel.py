from sentinel.sentinel import Sentinel
from sentinel.database.services import SQLite3


def test_create_db_service():
    db_url = 'sqlite://:memory:'
    sentinel = Sentinel()
    sentinel.db_config(db_url)
    assert isinstance(sentinel.db, SQLite3)
