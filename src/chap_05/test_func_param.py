import pytest
from cards import Card


@pytest.mark.parametrize(
    ["summary", "status"],  ## "summary, status", という文字列でもOK
    [
        ("write a book", "done"),  ## リストかタプルで
        ("second edition", "in prog"),
        ("create a course", "todo"),
    ],
)
def test_finish(cards_db, summary, status):
    init_card = Card(summary=summary, state=status)
    index = cards_db.add_card(init_card)
    cards_db.finish(index)
    c = cards_db.get_card(index)
    assert c.state == "done"


# status だけわかればそれでいい
@pytest.mark.parametrize("status", ["done", "in prog", "todo"])
def test_finish_status_only(cards_db, status):
    # summary はハードコード
    init_card = Card(summary="Write a code", state=status)
    index = cards_db.add_card(init_card)
    cards_db.finish(index)
    c = cards_db.get_card(index)
    assert c.state == "done"

