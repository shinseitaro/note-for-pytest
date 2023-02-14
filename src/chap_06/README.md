# chapter 06 memo
## マーカーとは
+ [@pytest.mark](https://docs.pytest.org/en/6.2.x/reference.html#marks)
+ pytest に、テスト関数が特別な意味や目的があることを伝える手段
+ タグやラベルのように考えてよし

## 組み込みマーカー
+ 色々あるけど、以下がよく使われる
    + [@pytest.mark.parametrize](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-parametrize)：テストに複数のパラメータを渡す（5章）
    + [@pytest.mark.skip](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-skip)：テストをスキップする
    + [@pytest.mark.skipif](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-skipif)：テストを条件付きでスキップする
    + [@pytest.mark.xfail](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-xfail)：テストが失敗することを想定する


### [@pytest.mark.skip](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-skip)：テストをスキップする
+ 使いみち：将来追加する機能のテストを先に作って置く
+  `src/chap_06/buildins/test_less_than.py` 
    ```python
    import pytest
    from cards import Card

    @pytest.mark.skip(reason="card の比較機能は未実装")
    def test_less_than():
        c1 = Card("a test")
        c2 = Card("b test")
        assert c1 < c2
    ```
    + 実行 
    ```bash
    ➜ pytest -v
    ============================================= test session starts ==============================================
    collected 1 item                                                                                               

    test_less_than.py::test_less_than SKIPPED (card の比較機能は未実装)                                      [100%]

    ============================================== 1 skipped in 0.02s ==============================================

    ```
    + `-ra` を入れると、成功したテスト以外の詳細を出力

    ```
    ➜ pytest -v -ra
    ============================================= test session starts ==============================================
    collected 1 item                                                                                               

    test_less_than.py::test_less_than SKIPPED (card の比較機能は未実装)                                      [100%]

    =========================================== short test summary info ============================================
    SKIPPED [1] test_less_than.py:5: card の比較機能は未実装
    ============================================== 1 skipped in 0.02s ==============================================

    ```

### [@pytest.mark.skipif](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-skipif)：テストを条件付きでスキップする
+ 使いみち：バージョン違いで機能が異なる場合など
+ [packaging · PyPI](https://pypi.org/project/packaging/)
+ `src/chap_06/buildins/test_skipif.py` 
    ```python
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

    ```

### [@pytest.mark.xfail](https://docs.pytest.org/en/6.2.x/reference.html#pytest-mark-xfail)：テストが失敗することを想定する
+ 使いみち：失敗するはずのテストが成功した場合、その結果をどのように表現するかを変えたい場合
    + XPASS：失敗するはずが成功しました。
    + FAILED：失敗するはずが成功しましたので、テストはFAILEDです。
+  `src/chap_06/buildins/test_xfail.py` 
    ```python
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
    @pytest.mark.xfail(reason="失敗予定が成功してしまうDemoテスト")
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

    ```
    ```bash
    ✗  pytest test_xfail.py -v
    ============================================= test session starts ==============================================
    collected 3 items                                                                                              

    test_xfail.py::test_less_than XFAIL (card の比較機能はver2以降で実装)                                    [ 33%]
    test_xfail.py::test_xpass_demo XPASS (失敗予定が成功したXPASS)                                           [ 66%]
    test_xfail.py::test_xfail_strict FAILED                                                                  [100%]

    =================================================== FAILURES ===================================================
    ______________________________________________ test_xfail_strict _______________________________________________
    [XPASS(strict)] 失敗予定が成功したのでテストはFAILED
    =========================================== short test summary info ============================================
    FAILED test_xfail.py::test_xfail_strict
    =================================== 1 failed, 1 xfailed, 1 xpassed in 0.04s ====================================
    ```
    +  `strict=True` の場合、テストが失敗しているので `FAILURES` に詳細が出る


## カスタムマーカー
+ 使いみち：ただ単に、テストにラベルやタグのようなものをつけたい。
+ 例：[スモークテスト](https://e-words.jp/w/%E3%82%B9%E3%83%A2%E3%83%BC%E3%82%AF%E3%83%86%E3%82%B9%E3%83%88.html)
    + スモークテストとは、もともと電子機器・電気機械の開発工程において、試作品の電源を投入してみて発煙しないか調べる試験。転じて、ソフトウェアでは、追加機能が既存機能を破壊していないかどうかなどの基本的なテストのことを言う
- `src/chap_06/smoke/test_smoke.py`
    ```python
    from pathlib import Path
    from tempfile import TemporaryDirectory

    import pytest
    from cards import Card, CardsDB, InvalidCardId


    @pytest.fixture()
    def cards_db():
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db = CardsDB(db_path)
            # ここで cards_dbデータは したのtest_empty に渡されて、テストが終わったらココに戻ってくる
            yield db 

            # 事後処理
            db.close()

    @pytest.mark.smoke ## たんなるラベルとして使用。ネーミングはご自由に
    def test_start(cards_db):
        i = cards_db.add_card(Card("foo", state="todo"))
        cards_db.start(i)
        c = cards_db.get_card(i)
        assert c.state == "in prog"

    def test_start_nonexistent(cards_db):
        n = 123 
        with pytest.raises(InvalidCardId):
            cards_db.start(n)        
    ```
    - 実行 `-m smoke` でカスタムマーカーをつけたテストだけ実行できる

    ```
    ✗  pytest test_smoke.py -v -m smoke
    ===================================== test session starts ======================================
    collected 2 items / 1 deselected / 1 selected                                                  

    test_smoke.py::test_start PASSED                                                         [100%]

    ======================================= warnings summary =======================================
    test_smoke.py:19
    src/chap_06/smoke/test_smoke.py:19: PytestUnknownMarkWarning: Unknown pytest.mark.smoke - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        @pytest.mark.smoke ## たんなるラベルとして使用。ネーミングはご自由に

    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    ========================== 1 passed, 1 deselected, 1 warning in 0.04s ==========================

    ```    
    +  `collected 2 items / 1 deselected / 1 selected ` と表示されている通り、smoke だけ実行された
    + `Unknown pytest.mark.smoke - is this a typo?  ` ：登録されていないカスタムマーカーはこのように警告が出る。登録は pytest.ini で行う
### pytest.ini
+ 設置場所はテストファイルがあるディレクトリ以上
+ 今回はchap06に置いた
+  `src/chap_06/pytest.ini`
    ```ini
    [pytest]
    markers = 
        smoke: subset of tests
    ``` 
### マーカーは複数つけることができる
```python 
@pytest.mark.<marker-name1>
@pytest.mark.<marker-name2>
def test_a():
    ....
```

### ファイルにカスタムマーカーをつける
```python 
# test_afile.py
import pytest
from cards import Card

pytestmark = pytest.mark.<marker-name>
# リストも可
pytestmark = [pytest.mark.<marker-name1>, pytest.mark.<marker-name2>, pytest.mark.<marker-name3>]
```

### クラスにカスタムマーカーをつける
```python 
import pytest
from cards import Card

@pytest.mark.<marker-name>
class TestSomething:
    def test_a():
        ....
```
### パラメタライズの一部にカスタムマーカーをつける
```python 
@pytest.mark.parametrize(
    ["summary", "status"],  
    [
        ("write a book", "done"),  
        pytest.param(("second edition", "in prog"), marks=pytest.mark.<marker-name>)
        ("create a course", "todo"),
    ],
)
def test_finish(cards_db, summary, status):
    ...
```

### 実行時に、and or not () で、マーカーをフィルタリングする
```bash
# 
pytest -v -m "marker-name1 and marker-name2"

# name1 だけど name2 がついていないテストを実行
pytest -v -m "marker-name1 and not marker-name2"


```

## マーカーとフィクスチャ
+ カスタムマーカは、パラメータを受け付けない
+ よって、パラメータを渡したい場合はフィクスチャとの組み合わせが必要
+ 例：
    + cards を db に n 個つくってカウントしたら n 個であるテストなど
+ イメージ：
    ```python 
    @pytest.mark.num_cards(3)
    def test_numcards(cards_db):
        assert cards_db.count() == 3
    ```
+ 手順
    1. フィクスチャを使うテストを作成
    1. マーカーを宣言
    1. フィクスチャを書き換えて、該当のマーカーが使用されたかどうかを検出するように更新
    1. マーカーにパラメータとして渡された値を読み取り、パラメータを使う
    + メモ：フェイクデータを作成する pytest フィクスチャを提供する、[Faker](https://pypi.org/project/Faker/)パッケージを使ってみます

### 1. フィクスチャを使うテストを作成 ＆ 2. マーカーを宣言
```python 
import pytest
from cards import Card, CardsDB


@pytest.fixture(scope="session")
def tmp_db_path(tmp_path_factory):
    return tmp_path_factory.mktemp("cards_db")


@pytest.fixture(scope="session")
def session_cards_db(tmp_db_path):
    db_ = CardsDB(tmp_db_path)
    yield db_
    db_.close()

@pytest.fixture(scope="function")
def cards_db(db):  
    return db

@pytest.mark.num_cards(3)
def test_numcards(cards_db):
    assert cards_db.count() == 3
```
typo だよって言われないように pytest.ini にも追加
```ini
[pytest]
markers = 
    smoke: subset of tests
    num_cards: number of card to prefill for cards_db fixture
```
### 3. フィクスチャを書き換えて、該当のマーカーが使用されたかどうかを検出するように更新
```python 
@pytest.fixture(scope="function")
def cards_db(session_cards_db, request, faker):
    db = session_cards_db
    # 一旦DBを空にする
    db.delete_all()
    # 乱数作成
    faker.seed_instance(101)
    m = request.node.get_closest_marker("num_cards")
    if m and len(m.args) > 0:
        num_cards = m.args[0]
        for _ in range(num_cards):
            db.add_card(
                Card(summary=faker.sentence(), 
                     owner=faker.first_name())
            )
    return db
```
` m = request.node.get_closest_marker("num_cards")` これでこのようなオブジェクトをえることができる
```
Mark(name='num_cards', args=(3,), kwargs={})
```
よって、 `m.args` で、最初の引数を得ることができる

### 4. マーカーにパラメータとして渡された値を読み取り、パラメータを使う

```python 
@pytest.mark.num_cards(3)
def test_numcards(cards_db):
    assert cards_db.count() == 3
    # faker が作ったデータを確認してみる
    for c in cards_db.list_cards():
        print(c)
```
```bash
pytest -s -v
================================================ test session starts ================================================
plugins: Faker-17.0.0
collected 1 item                                                                                                    

Card(summary='Suggest training much grow any me own true.', owner='Todd', state='todo', id=1)
Card(summary='Forget just effort claim knowledge.', owner='Amanda', state='todo', id=2)
Card(summary='Line for PM identify decade.', owner='Russell', state='todo', id=3)
PASSED

================================================= 1 passed in 0.06s =================================================
```


## その他のメモ
+ `pytest --markers` で配下で使ってるマーカーを確認できます
+ `pytest.ini` に下記を追加しておくことも可
    ```ini
    addopts = 
        --strict-markers # フラグ。宣言されていないマーカーを使っている場合はエラーを返す
        --ra # フラグ。テストが成功しない理由を出力
    xfail_strict = true # xfail を参照
    ```

