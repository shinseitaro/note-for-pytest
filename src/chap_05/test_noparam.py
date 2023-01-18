from cards import Card


def test_finish_from_in_prog(cards_db):
    index = cards_db.add_card(Card("second edition", state="in prog"))
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


def test_finish_from_in_done(cards_db):
    index = cards_db.add_card(Card("something", state="done"))
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


def test_finish_from_todo(cards_db):
    index = cards_db.add_card(Card("anything", state="todo"))
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
