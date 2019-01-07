from sentinel.database import manager
from sentinel.database.services import SQlite3

import pytest


DB_NAME = ':memory:'


@pytest.fixture(scope="module")
def db_service(request):
    db = manager(f"sqlite://{DB_NAME}")

    def fin():
        db.close()
    request.addfinalizer(fin)
    return db


def test_is_sqlite_instance(db_service):
    assert isinstance(db_service, SQlite3)


def test_create_the_rule_table(db_service):
    db_service.migrate()

    cursor = db_service.conn.cursor()
    query = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='rules';
    """)
    results = query.fetchone()
    assert len(results) > 0


# def test_add_rules(db_service):
#     db_service.add_rule()
