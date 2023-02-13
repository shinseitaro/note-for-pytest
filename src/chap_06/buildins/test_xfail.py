import cards
import pytest
from cards import Card
from packaging.version import parse


# 失敗することを想定しているテスト
@pytest.mark.xfail(
    parse(cards.__version__).major < 2, 
    reason="card の比較機能はver2以降で実装"
)
def test_less_than():
    c1 = Card("a test")
    c2 = Card("b test")
    assert c1 < c2


# 失敗することを想定していたが成功したときのデモ
@pytest.mark.xfail(reason="失敗予定が成功したXPASS")
def test_xpass_demo():
    c1 = Card("A")
    c2 = Card("A")
    assert c1 == c2 

# 失敗することを想定していたが成功したとき、XFAIL ではなく FAILED を出すデモ
@pytest.mark.xfail(reason="失敗予定が成功したのでテストはFAILED", strict=True)
def test_xfail_strict():
    c1 = Card("A")
    c2 = Card("A")
    assert c1 == c2 

