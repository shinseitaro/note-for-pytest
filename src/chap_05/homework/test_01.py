# stateがどの状態から始まっても start()が呼ばれると in prog になることを確認するテスト

from cards import Card


def test_start_from_done(cards_db):
    index = cards_db.add_card(Card("second edition", state="done"))
    cards_db.start(index)
    card = cards_db.get_card(index)
    assert card.state == "in prog"


def test_start_from_in_prog(cards_db):
    index = cards_db.add_card(Card("second edition", state="in prog"))
    cards_db.start(index)
    card = cards_db.get_card(index)
    assert card.state == "in prog"


def test_start_from_todo(cards_db):
    index = cards_db.add_card(Card("second edition", state="todo"))
    cards_db.start(index)
    card = cards_db.get_card(index)
    assert card.state == "in prog"
