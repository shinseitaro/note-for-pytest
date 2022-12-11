# chapter 03 memo

- fixture: 実際のテスト関数の実行に先立って、Pytestが実行する関数
    - テスト用データ読み込みなど

```python 
import pytest

@pytest.fixture() 
def some_data():
    return 42

def test_some_data(some_data):
    assert some_data == 42
```
+ 事前作業
    + `@pytest.fixture()` で fixure に登録
+ テスト
    + fixureの名前を渡されたテスト関数は、まずfixtureを実行してからテストを実行する
    + その際、fixure が持つデータを、そのfixtureの名前で利用できる
+ 例外
    + テストコードの実行中の例外：`pytest.failed` `AssertionError` `=== FAILURES ===` 
    + フィスクチャの実行中の例外：`ERRORS`  `==== ERRORS ====`
    
+ 注意
    +  `fixure` という言葉の使い方が様々なので臨機応変に使って。（Python 界隈の話だけではなくプログラミングコミュニティ全体的に様々）
    + ここでは
        +  `@pytest.fixture()` で修飾されたものはいずれかで呼んでいる
        + フィクスチャ
        + フィクスチャ関数
        + フィクスチャメソッド
    +  `テストフィクスチャ`
        + 前処理後処理を、テスト関数から切り離すためのPytestのメカニズムのこと


