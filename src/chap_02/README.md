# chapter 02 memo

[Python Testing with pytest, Second Edition: Simple, Rapid, Effective, and Scalable by Brian Okken](https://pragprog.com/titles/bopytest2/python-testing-with-pytest-second-edition/)

## 2022/11/30 yattom さんの話
+ Chapter02に全てが書いてある
+ その後は、その他便利な使い方が書いてある
+ フィクスチャはとてもよい
+ 7章はPytestの話ではなく、テストの考え方。テスターとプログラマーの橋渡しになる章

## 以下メモ

+ インストール時エラー
    ```bash
    pip install code/cards_proj/

    ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
    black 22.10.0 requires click>=8.0.0, but you have click 7.1.2 which is incompatible.
    ```
    - card をインストールする前に、blackをインストールしてたら↑のエラーがでたので、venv 作り直してインストールしなおしました。


- `db.py` 
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

- `with pytest.raises(TypeError):` 
    - 次のコードブロックの何かがTypeErrorを発生させるハズという意味
    - 発生しないと失敗しない
- `with pytest.raises(TypeError, match=match_regex):` 
    - 例外メッセージの照合
    - 今回のエラーメッセージは、 `TypeError: __init__() missing 1 required positional argument: 'db_path'`  
    ```python 
    def test_raises_with_info():
        match_regex = "missing 1 .* positional argument"
        with pytest.raises(TypeError, match=match_regex):
            cards.CardsDB()    
    ```
- `with pytest.raises(TypeError) as exc_info:` 
    - 変数 (`exc_info` ) で引き取ることも出来る

- `Given - When - Then` 
    1. Given 振る舞いを実行する前の状態を記述(データ、環境)
    2. When 振る舞いを記述
    3. Then 振る舞いの結果を記述

- pytest -v src/chap_02/test_classes.py::<クラス名>
    - １クラスのテスト実行
    - `-k` オプションはテスト名のパターンマッチング。よってクラス名を指定するとそのクラスだけテストする。
    ```bash 
    > cd src/chap_02/
    > pytest -v -k TestEquality
    ```
    + その他一部実行方法は P30 参照

## 章末問題
1. 
    ```python
    @dataclass
    class Card:
        summary: str = ""
        owner: str = ""
        state: str = "todo"
        id: int = field(default=None, compare=False)
    ``` 
    ```
        def test_defaults():
            c = Card()
    >       assert c.summary is None
    E       AssertionError: assert '' is None
    E        +  where '' = Card(summary='', owner='', state='todo', id=None).summary

    test_card_mod.py:31: AssertionError
    ```
1.  c1 と c2 は identical じゃないと怒られる
    ```
        def test_equality_with_diff_ids():
            c1 = Card("something", "brian", "todo", 123)
            c2 = Card("something", "brian", "todo", 4567)
    >       assert c1 == c2
    E       AssertionError: assert Card(summary=...todo', id=123) == Card(summary=...odo', id=4567)
    E         
    E         Omitting 3 identical items, use -vv to show
    E         Differing attributes:
    E         ['id']
    E         
    E         Drill down into differing attribute id:
    E           id: 123 != 4567

    ```
1.  compare=False に戻して、id が None でも 同じカードとみなすか
    ```python 
    def test_equality_with_diff_ids():
        c1 = Card("something", "brian", "todo", 123)
        c2 = Card("something", "brian", "todo", 4567)
        c3 = Card("something", "brian", "todo")

        assert c1 == c2
        assert c1 == c3
    ```
1. 
    ```bash 
    > pytest test_card_mod.py -k dict  -vv
    =================================================================== test session starts ===================================================================
    platform linux -- Python 3.8.3, pytest-7.2.0, pluggy-1.0.0 -- /home/shinseitaro/workspace/github/finpy/note-for-pytest/.venv/bin/python
    cachedir: .pytest_cache
    rootdir: /home/shinseitaro/workspace/github/finpy/note-for-pytest/src/chap_02
    collected 7 items / 5 deselected / 2 selected                                                                                                             

    test_card_mod.py::test_from_dict PASSED                                                                                                             [ 50%]
    test_card_mod.py::test_to_dict PASSED                                                                                                               [100%]

    ============================================================= 2 passed, 5 deselected in 0.01s =============================================================


    ```

