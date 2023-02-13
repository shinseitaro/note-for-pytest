import cards
import pytest
from cards import Card
from packaging.version import parse


@pytest.mark.skipif(
    parse(cards.__version__).major < 2, 
    reason="card の比較機能はver2以降で実装"
)
def test_less_than():
    c1 = Card("a test")
    c2 = Card("b test")
    assert c1 < c2
