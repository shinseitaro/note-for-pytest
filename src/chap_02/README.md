# chapter 02 memo

[Python Testing with pytest, Second Edition: Simple, Rapid, Effective, and Scalable by Brian Okken](https://pragprog.com/titles/bopytest2/python-testing-with-pytest-second-edition/)

```bash
pip install code/cards_proj/

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
black 22.10.0 requires click>=8.0.0, but you have click 7.1.2 which is incompatible.
```

venv 作り直してインストールしなおし


`db.py` 

- [Welcome to TinyDB! — TinyDB 4.7.0 documentation](https://tinydb.readthedocs.io/en/latest/)
    - sqlite3 の ドキュメント指向(Document Oriented あらゆるドキュメントを格納可) DBという感じ

- `api.py`
```python 
@dataclass
class Card:
    summary: str = None
    owner: str = None
    state: str = "todo"
    id: int = field(default=None, compare=False)
```
    - カードオブジェクト同士が同じかどうかを確認する時に、 **`id` は使わない** ようにするために、field メソッドを使って、 option `compare=False` を渡している

`-vv`
    ```
    pytest src/chap_02/test_card_fail.py -vv
    ```
    - どの属性でエラーがでたのか詳細確認出来る

- `pytest.fail()`
    - わざとテストを失敗させたい時

- `__tracebackhide__ = True` 
    ```python 
    def assert_identical(c1: Card, c2: Card):
        __tracebackhide__ = True
        assert c1 == c2
        if c1.id != c2.id:
            pytest.fail(f"id's don't match. {c1.id} != {c2.id}")

    def test_identical():
        c1 = Card("foo", id=123)
        c2 = Card("foo", id=456)
        assert_identical(c1, c2)
    ```
    - この場合は、id が違うときにテストを失敗させたいので、 `test_identical`テストの結果だけ失敗したことを教えてほしい。つまりヘルパーである `assert_identical` の結果はいらない。こういう時に `__tracebackhide__ = True` 