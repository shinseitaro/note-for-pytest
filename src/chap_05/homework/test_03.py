import pytest
from cards import Card


@pytest.fixture(params=["done", "in prog", "todo"])
def start_state(request):
    return request.param


def test_start(cards_db, start_state):
    init_card = Card(summary="hoge moge", state=start_state)
    idx = cards_db.add_card(init_card)
    cards_db.start(idx)
    c = cards_db.get_card(idx)
    assert c.state == "in prog"

