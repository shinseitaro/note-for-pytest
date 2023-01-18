import cards
import pytest


@pytest.fixture(scope="session")
def db(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("cards_db")
    db_ = cards.CardsDB(db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db(db):
    db.delete_all()
    return db

