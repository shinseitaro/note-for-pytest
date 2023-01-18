from cards import Card


def pytest_generate_tests(metafunc):
    if "state" in metafunc.fixturenames:
        metafunc.parametrize("state", ["done", "in prog", "todo"])


def test_start(cards_db, state):
    init_card = Card(summary="hoge moge", state=state)
    idx = cards_db.add_card(init_card)
    cards_db.start(idx)
    c = cards_db.get_card(idx)
    assert c.state == "in prog"
