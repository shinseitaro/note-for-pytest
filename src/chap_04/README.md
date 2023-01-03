# chapter 04 memo

組み込みフィクスチャを3つ

+ tmp_path, temp_path_factory
    + 一時ディレクトリ取得
    + tmp_path は関数スコープ
    + temp_path_factory はセッションスコープ
+ capsys
    1. stdout / stderr をキャプチャ
    1. 出力キャプチャを一時的に無効にする
+ monkeypatch 
    + アプリケーションコードや環境を変更


### tmp_path, temp_path_factory
+ 一時ディレクトリ取得
+ テストで直接使う分にはほとんど同じ様に使用可
```python 
# tmp_path は、pathlib.Path オブジェクト
def test_tmp_path(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"

# tmp_path_factory は、TempPathFactoryオブジェクト.
def test_tmp_path_factory(tmp_path_factory):
    path = tmp_path_factory.mktemp("sub") #mktempで一時パスを取得するい必要がある
    file = path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"
```
+ しかし、フィクスチャの中で使う時はスコープの違いに注意

+ temp_path_factory はセッションスコープ
    + 一時ディレクトリ取得のために `.mktemp()` メソッドを使う
    + この一時ディレクトリはセッションが終わった後一定時間残るのでテスト失敗時にディレクトリを確認することも可（Pytestが直近数回分のディレクトリを残す機能を利用）
    ```python 
    @pytest.fixture(scope="session")
    def db(tmp_path_factory):
        db_path = tmp_path_factory.mktemp("cards_db")
        db_ = cards.CardsDB(db_path)
        yield db_
        db_.close()
    ```
+ tmp_path は関数スコープ
    ```python 
    @pytest.fixture(scope="function")
    def cards_db(db): ## ↑で作った db を引き込んで使っている
        db.delete_all()
        return db
    ```
+ 続きは `./conftest.py` 

### capsys
#### 1. stdout / stderr をキャプチャ
+ version 確認テスト
    ```python 
    import cards
    def test_version_v2(capsys):
        # cards.cli.version()
        output = capsys.readouterr().out.rstrip()
        assert output == cards.__version__
    ```
+ エラーメッセージテスト

#### 2. 出力キャプチャを一時的に無効にする
+ 以下の例だとPytestが出力をキャプチャしてしまうので、成功時にはprintされない
    ```python 
    def test_fail():
        # これだと
        print("\nnormal print")
    ```
+ 成功時にもPrint関数の出力を表示するために `capsys.disabled()` コンテキストマネージャを使う
    ```python 
    def test_disabled(capsys):
        with capsys.disabled():
            print("\ncapsys disabled print")
    ```


### monkeypatch 

- アプリケーションコードや環境を変更
- 教科書の説明が理解しづらかったので、コレを参照した
    - [hawksnowlog: pytest の monkeypatch を使って簡単モック作成](https://hawksnowlog.blogspot.com/2020/07/monkeypatch-with-pytest.html)

```python 
class User():
    FAVORITE_FRAMEWORKS = {
        "ruby": "sinatra",
        "swift": "spritekit",
        "python": "flask"
    }

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def hello(self):
        return("%s,%i" % (self.name, self.age))

```
テスコトード
```python 
from user import User

def test_hello(monkeypatch):
    # hello メソッドにパッチを当ててレスポンスを操作する
    monkeypatch.setattr(User, "hello", lambda self: "hawksnowlog,5")
    u = User("hawksnowlog", 10)
    assert(u.hello() == "hawksnowlog,5")
```
+ `monkeypatch.setattr(クラス名, メソッド名, モック)`
- 環境変数をテスト時に上書きすることが出来る
+ モックは、callable である必要がある
