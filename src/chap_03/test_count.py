from pathlib import Path
from tempfile import TemporaryDirectory
import cards

import pytest


@pytest.fixture()
def cards_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)

        # ここで cards_dbデータは したのtest_empty に渡されて、テストが終わったらココに戻ってくる
        yield db

        # 事後処理
        db.close()


def test_empty(cards_db):
    assert cards_db.count() == 0


def test_two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("second"))
    assert cards_db.count() == 2

