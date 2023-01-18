# chapter 05 memo

## パラメータ化

関数をテストしたい場合、複数の異なるデータを渡してテストを行いたい場合がある。その時に pytest では
+ 関数のパラメータ化する
+ フィクスチャをパラメータ化する
+ フック関数 [pytest_generate_tests](https://docs.pytest.org/en/6.2.x/reference.html?highlight=pytest_generate_tests#pytest.hookspec.pytest_generate_tests) を使う
の三つの方法がある

### 0. パラメータ無しテスト
- 事前準備 : src/chap_05/conftest.py
- テスト内容： `cards_db.finish()` したら、カードのステイタスが "done"になることを確認
- コード
    ```python
    from cards import Card


    def test_finish_from_in_prog(cards_db):
        index = cards_db.add_card(Card("second edition", state="in prog"))
        cards_db.finish(index)
        card = cards_db.get_card(index)
        assert card.state == "done"


    def test_finish_from_in_done(cards_db):
        index = cards_db.add_card(Card("write a book", state="done"))
        cards_db.finish(index)
        card = cards_db.get_card(index)
        assert card.state == "done"


    def test_finish_from_todo(cards_db):
        index = cards_db.add_card(Card("create a course", state="todo"))
        cards_db.finish(index)
        card = cards_db.get_card(index)
        assert card.state == "done"

    ```
+ 改善ポイント
    + in prog / done / todo と　テキスト部分以外は全部一緒なので冗長
    + このデータ部分をパラメータ化したい
    + `cards_db.add_card()` をリスト化して for で回すという手もあるけど、テストが１つになってしまってコケた場合どこでコケたかわからないなどの不都合がある。

### 1. 関数のパラメータ化する
- 指定した引数セット（データセット）ごとに pytest が関数を呼び出す形でテストを行う
+ `@pytest.mark.parametrize` マーカー
+ [@pytest.mark.parametrize: parametrizing test functions — pytest documentation](https://docs.pytest.org/en/6.2.x/parametrize.html#pytest-mark-parametrize)
    ```python 
    @pytest.mark.parametrize(
        ["arg1", "arg2", "arg3"], ## 関数に渡す引数をリストもしくはコンマ区切りの文字列で渡す。
        [
            (data1, data2, data3), ## タプルもくしはリストでテストデータを渡す
            (data1, data2, data3),
            (data1, data2, data3),
        ])
    def test_foo(arg1, arg2, arg3):
        ,,,,,
    ```
- 例： src/chap_05/test_func_param.py
    ```python 
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

    ```
- 実行
    ```bash 
    # -v を忘れずにつける
    > pytest test_func_param.py -v
    ====== test session starts ======                                                         

    test_func_param.py::test_finish[write a book-done] PASSED [ 33%]
    test_func_param.py::test_finish[second edition-in prog] PASSED [ 66%]
    test_func_param.py::test_finish[create a course-todo] PASSED  [100%]

    ======= 3 passed in 0.02s =======

    ```
    - データ毎にテスト結果を出力
    - `test_func_param.py::test_finish[write a book-done] ` 
    - ただ、`[write a book-done]`は、ステイタスだけ表示されれば別にいい。よって次の様に書ける
- シンプルにした書き方    
    ```python 
    # status だけわかればそれでいい
    @pytest.mark.parametrize("status", ["done", "in prog", "todo"])
    def test_finish_status_only(cards_db, status):
        # summary はハードコード
        init_card = Card(summary="Write a code", state=status)
        index = cards_db.add_card(init_card)
        cards_db.finish(index)
        c = cards_db.get_card(index)
        assert c.state == "done"
    ```
+ 実行
    ```bash 
    ❯ pytest test_func_param.py::test_finish_status_only -v
    ===== test session starts ====                

    test_func_param.py::test_finish_status_only[done] PASSED  [ 33%]
    test_func_param.py::test_finish_status_only[in prog] PASSED [ 66%]
    test_func_param.py::test_finish_status_only[todo] PASSED [100%]

    ====== 3 passed in 0.02s ======

    ```
### 2. フィクスチャをパラメータ化する
+ テストデータをフィクスチャに移動させる
    ```python 
    @pytest.fixture(params=["done", "in prog", "todo"])
    def start_state(request):
        return request.param
    ```
+ フィクスチャに依存しているテスト関数を書く
    ```python 
    def test_finish(cards_db, start_state):
        init_card = Card("write a book", state=start_state)
        index = cards_db.add_card(init_card)
        cards_db.finish(index)
        c = cards_db.get_card(index)
        assert c.state == "done"
    ```
+ フィクスチャにのテストデータごとにテスト関数が呼び出される
+ 実行
    ```bash 
    ===== test session starts =====
    test_fix_param.py::test_finish[done] PASSED [ 33%]
    test_fix_param.py::test_finish[in prog] PASSED [ 66%]
    test_fix_param.py::test_finish[todo] PASSED [100%]
    ====== 3 passed in 0.02s ======

    ```
- [request — pytest documentation](https://docs.pytest.org/en/7.1.x/reference/reference.html?highlight=metafunc#request)

### 3. フック関数 pytest_generate_tests を使う

+ [フックとは](https://wa3.i-3-i.info/word12296.html)
    > プログラムの中に独自の処理を割りこませるために用意されている仕組み。
    > もしくは
    > プログラムにおいて、本来の処理を横取りして独自の処理を割りこませること

- [第一級オブジェクト - Wikipedia](https://ja.wikipedia.org/wiki/%E7%AC%AC%E4%B8%80%E7%B4%9A%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88)
- 実装
    ```python 
    def pytest_generate_tests(metafunc):
        if "start_state" in metafunc.fixturenames:
            metafunc.parametrize("start_state", ["done", "in prog", "todo"])

    def test_finish(cards_db, start_state):
        init_card = Card("write a book", state=start_state)
        index = cards_db.add_card(init_card)
        cards_db.finish(index)
        c = cards_db.get_card(index)
        assert c.state == "done"
    ```
- `pytest_generate_tests` と `metafunc` は、pytest をインストールした環境下では first class として使えるみたい
    - [Basic pytest_generate_tests example — pytest documentation](https://docs.pytest.org/en/6.2.x/parametrize.html#pytest-generate-tests)
    - [def pytest_generate_tests](https://github.com/pytest-dev/pytest/blob/9fbd67dd4b1baa6889dbb2073c17b85da39f80d9/src/_pytest/python.py#L149)
    - [class FixtureManager / pytest_generate_tests](https://github.com/pytest-dev/pytest/blob/791b51d0faea365aa9474bb83f9cd964fe265c21/src/_pytest/fixtures.py#L1543)
- metafunc は、`pytest_generate_tests` に渡すオブジェクトとして定義されていて、ここでは `parametrize` メソッドを呼び出して、 `@pytest.mark.parametrize("status", ["done", "in prog", "todo"])` みたいに使っている
    - パラメータが２つ以上ある場合も同様に書ける
    ```python 
    metafunc.paramtrize(
                "summary, status",
                [
                    ("write a book", "done"),
                    ("second edition", "in prog"),
                    ("create a course", "todo"),
                ],
            )
    ```
    + metafunc で使える、メソッドや属性は、[Metafunc — pytest documentation](https://docs.pytest.org/en/7.1.x/reference/reference.html?highlight=metafunc#metafunc)で確認して
    - ソースはここ : [class Metafunc](https://github.com/pytest-dev/pytest/blob/9fbd67dd4b1baa6889dbb2073c17b85da39f80d9/src/_pytest/python.py#L1183)


