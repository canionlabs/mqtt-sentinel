from sentinel.database import DBManager


def test_create_manager():
    manager = DBManager("postgres://USER:PASSWORD@HOST:PORT/NAME")
    assert isinstance(manager, DBManager)
