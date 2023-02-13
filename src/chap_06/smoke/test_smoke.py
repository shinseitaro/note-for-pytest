from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from cards import Card, CardsDB, InvalidCardId


@pytest.fixture()
def cards_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = CardsDB(db_path)
        # ここで cards_dbデータは したのtest_empty に渡されて、テストが終わったらココに戻ってくる
        yield db 

        # 事後処理
        db.close()

@pytest.mark.smoke ## たんなるラベルとして使用。ネーミングはご自由に
def test_start(cards_db):
    i = cards_db.add_card(Card("foo", state="todo"))
    cards_db.start(i)
    c = cards_db.get_card(i)
    assert c.state == "in prog"

def test_start_nonexistent(cards_db):
    n = 123 
    with pytest.raises(InvalidCardId):
        cards_db.start(n)

    


