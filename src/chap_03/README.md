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

## まとめ

### フィクスチャは、 return  / yield を使ってデータを返すことが出来る
- yield の場合： yield 前のコードがセットアップ、後がティアダウン。これを使うと、テストとセットアップ、ティアダウンをキレイに分けることが出来る
- 例：初期設定と事後処理が、テストに混ざって汚い
    ```python 
    # 初期設定と事後処理が、テストに混ざって汚い
    def test_empty():
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db = cards.CardsDB(db_path)

            count = db.count()
            db.close()

            assert count == 0

    ```
+ キレイに分ける
    ```python 
    @pytest.fixture()
    def cards_db():
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db = cards.CardsDB(db_path)
            # ここで cards_dbデータは したのtest_empty に渡されて、テストが終わったらココに戻ってくる
            yield db 

            # 事後処理
            db.close()

    def test_empty(cards_db):
        assert cards_db.count() == 0
    ```

### フィクスチャのスコープ
+ 同じフィクスチャを使う場合、通常、テスト関数単位でフィクスチャは呼び出される。したがってこのようにテストを行うと、上記の fixtureを二回行うことになる。
    ```python 
    def test_two(cards_db):
        cards_db.add_card(cards.Card("first"))
        cards_db.add_card(cards.Card("second"))
        assert cards_db.count() == 2
    ```
+ テストの独立性は保てるけど、時間がかかる事もある。そういう場合は `@pytest.fixture(scope="スコープ名")` でスコープ指定
+ デフォルトは `scope="function"` 
    ```python 
    @pytest.fixture(scope="module")
    def cards_db():
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db = cards.CardsDB(db_path)
            yield db
            db.close()

    ```
+ `--setup-show` を使うとテストの順番を表示するので、セットアップやティアダウンがいつ行われているのかも確認出来る
+ 例：`@pytest.fixture()` のテスト
    ```bash 
    > pytest --setup-show src/chap_03/test_count.py 
    src/chap_03/test_count.py 
            SETUP    F cards_db
            src/chap_03/test_count.py::test_empty (fixtures used: cards_db).
            TEARDOWN F cards_db
            SETUP    F cards_db
            src/chap_03/test_count.py::test_two (fixtures used: cards_db).
            TEARDOWN F cards_db
    ```
+ 例：`@pytest.fixture(scope="module")` のテスト
    ```bash 
    > pytest --setup-show src/chap_03/test_mod_scope.py 
    src/chap_03/test_mod_scope.py 
        SETUP    M cards_db
            src/chap_03/test_mod_scope.py::test_empty (fixtures used: cards_db).
            src/chap_03/test_mod_scope.py::test_non_empty (fixtures used: cards_db).
        TEARDOWN M cards_db

    ```
+ その他の指定
    + `@pytest.fixture(scope="class")` 
    + `@pytest.fixture(scope="package")` 
    + `@pytest.fixture(scope="session")` 

### `conftest.py` にフィクスチャを書くと、複数のテストモジュールで使用可
+ 複数のテストファイルでフィクスチャを共有したい場合 `conftest.py` にフィクスチャを定義
+ 注意： pytest が `conftest.py` を探すので ** `conftest.py` を import して使う事はしない**
+ 探す場所は、
    + テスト関数と同じディレクトリ
    + テストルートからテスト関数までの親ディレクトリ
+ どのフィクスチャを使っているか調べる
    ```bash 
    cd テストファイルディレクトリ
    pytest --fixtures -v 
    ```
### スコープの異なるフィクスチャを使う
+ 「db を一度だけ開いて、テスト前に必ずdbを空の状態にしたい」というようなセットアップの場合、あるフィクスチャに別のフィクスチャを依存させる方法を使う。テストの高速化も出来る。
    ```python 
    @pytest.fixture(scope="session")
    def db():
        """CardsDB object connected to a temporary database"""
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db_ = cards.CardsDB(db_path)
            yield db_
            db_.close()

    # 上のフィクスチャに依存しているフィクスチャ
    @pytest.fixture(scope="function") # function なので session より狭い
    def cards_db(db): # db を取り込んでテストを行う
        """CardsDB object that's empty"""
        db.delete_all()
        return db
    ```
+ テスト
    ```python 
    import cards

    def test_two(cards_db):
        cards_db.add_card(cards.Card("first"))
        cards_db.add_card(cards.Card("second"))
        assert cards_db.count() == 2
    ```

+ **注意**
    - 他のフィクスチャに依存するフィクスチャは、自分と同じもしくは狭いスコープのフィクスチャでなくてはいけない
    - ここでは、`cards_db` は `function` で、取り込んでいる `db` は `session` なので依存可

### 複数のフィクスチャを使う
+ `non_empty_db` 関数のように複数のフィクスチャを引数にとることが出来る
+ ただし、引数のフィクスチャの中で**最小のスコープに合わせなくてはならない**
    ```python 
    @pytest.fixture(scope="session")
    def db():
        """CardsDB object connected to a temporary database"""
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db_ = cards.CardsDB(db_path)
            yield db_
            db_.close()


    @pytest.fixture(scope="function")
    def cards_db(db):
        """CardsDB object that's empty"""
        db.delete_all()
        return db


    @pytest.fixture(scope="session")
    def some_cards():
        """List of different Card objects"""
        return [
            cards.Card("write book", "Brian", "done"),
            cards.Card("edit book", "Katie", "done"),
            cards.Card("write 2nd edition", "Brian", "todo"),
            cards.Card("edit 2nd edition", "Katie", "todo"),
        ]

    # cards_db のスコープがfunctionなので、それに合わせなくてはいけない
    @pytest.fixture(scope="function")
    def non_empty_db(cards_db, some_cards): 
        """CardsDB object that's been populated with 'some_cards'"""
        for c in some_cards:
            cards_db.add_card(c)
        return cards_db

    ```
### スコープを動的に決めたい
1. スコープを決める関数を作成
    ```python 
    def db_scope(fixture_name, config):
        if config.getoption("--func-db", None):
            return "function"
        return "session"
    ```
1. pyteset コマンドラインから使えるように追加
    ```python 
    def pytest_addoption(parser):
        parser.addoption(
            "--func-db", action="store_true", default=False, help="new db for each test",
        )
    ```
1. fixture に スコープを決める関数名を指定
    ```python
    @pytest.fixture(scope=db_scope)
    def db():
        """CardsDB object connected to a temporary database"""
        with TemporaryDirectory() as db_dir:
            db_path = Path(db_dir)
            db_ = cards.CardsDB(db_path)
            yield db_
            db_.close()
    ```

### autouse 
- `@pytest.fixture(autouse=True)` 
- テスト関数やフィクスチャに呼び出されなくても、常に実行されるフィクスチャ

### フィクスチャ名を変更
```python 
@pytest.fixture(name="ultimate_answer")
def ultimate_answer_fixture():
    return 42

def test_everything(ultimate_answer):
    assert ultimate_answer == 42
```


