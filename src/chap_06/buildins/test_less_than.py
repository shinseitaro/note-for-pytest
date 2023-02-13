import pytest
from cards import Card


@pytest.mark.skip(reason="card の比較機能は未実装")
def test_less_than():
    c1 = Card("a test")
    c2 = Card("b test")
    assert c1 < c2
