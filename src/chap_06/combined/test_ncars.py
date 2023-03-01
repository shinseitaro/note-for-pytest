import pytest
from cards import Card, CardsDB

# https://faker.readthedocs.io/en/master/pytest-fixtures.html
# locale もある！面白い
@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return [
        "ja_JP",
        "it_IT",
    ]


@pytest.fixture(scope="session")
def tmp_db_path(tmp_path_factory):
    return tmp_path_factory.mktemp("cards_db")


@pytest.fixture(scope="session")
def session_cards_db(tmp_db_path):
    db_ = CardsDB(tmp_db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db(session_cards_db, request, faker):
    db = session_cards_db
    # 一旦DBを空にする
    db.delete_all()
    # 乱数作成
    faker.seed_instance(101)
    m = request.node.get_closest_marker("num_cards")

    print("request.node", request.node)
    print("m", m)

    if m and len(m.args) > 0:
        num_cards = m.args[0]
        for _ in range(num_cards):
            db.add_card(Card(summary=faker.sentence(), owner=faker.first_name()))
    return db


@pytest.mark.num_cards(3)
def test_numcards(cards_db):
    assert cards_db.count() == 3
    for c in cards_db.list_cards():
        print(c)

