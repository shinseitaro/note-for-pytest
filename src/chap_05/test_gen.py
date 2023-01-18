from cards import Card


def pytest_generate_tests(metafunc):
    if "start_state" in metafunc.fixturenames:
        metafunc.parametrize("start_state", ["done", "in prog", "todo"])


def test_finish(cards_db, start_state):
    init_card = Card("write a book", state=start_state)
    index = cards_db.add_card(init_card)
    cards_db.finish(index)
    c = cards_db.get_card(index)
    assert c.state == "done"
