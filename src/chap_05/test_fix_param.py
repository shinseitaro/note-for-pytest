import pytest
from cards import Card


@pytest.fixture(params=["done", "in prog", "todo"])
def start_state(request):
    return request.param


def test_finish(cards_db, start_state):
    init_card = Card("write a book", state=start_state)
    index = cards_db.add_card(init_card)
    cards_db.finish(index)
    c = cards_db.get_card(index)
    assert c.state == "done"

