from pathlib import Path
from tempfile import TemporaryDirectory
import cards
import pytest


@pytest.fixture(scope="session")
def db():
    """CardsDB object connected to a temporary database"""
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db_ = cards.CardsDB(db_path)
        yield db_
        db_.close()


# 上のフィクスチャに依存しているフィクスチャ
@pytest.fixture(scope="function")
def cards_db(db):  # db を取り込んでテストを行う
    """CardsDB object that's empty"""
    db.delete_all()
    return db
