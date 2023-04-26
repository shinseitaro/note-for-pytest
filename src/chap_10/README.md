# chapter 10 memo

## モックとモックアップの違い

ChatGPT に聞きました。

+ モック: テストの中で他のオブジェクトや関数を置き換えるために使う。**正確な振る舞いをシミュレート**するために使うが、通常は**実際のオブジェクトや関数とは異なる実装**を持つ。モックを使用することで、テストの実行時に、外部のリソースや依存関係のあるオブジェクトを使用しなくてもよいという利点がある。

+ モックアップは、テストの中で他のオブジェクトを置き換えるために使用されるが、モックとは異なり、通常は**実際のオブジェクトと同じ実装**を持つ。つまり、モックアップは、通常、**テスト環境の中で使用する本物のオブジェクトの代替品**

```python 
# モックの例
from unittest.mock import Mock

# モックオブジェクトの作成
mock_obj = Mock()
mock_obj.method1.return_value = "result"

# モックを使用するテスト
def test_using_mock():
    # method1が呼び出されたことを確認
    mock_obj.method1.assert_called_once()

    # method1の戻り値が"result"であることを確認
    assert mock_obj.method1() == "result"
```
```python
# モックアップの例
class Database:
    def connect(self):
        pass

class TestDatabase:
    def connect(self):
        return "test connection"

# モックアップを使用するテスト
def test_using_mockup():
    # テスト用のオブジェクトを作成
    db = TestDatabase()

    # connectメソッドが呼び出されたときに、"test connection"を返すようにモックアップする
    db.connect = lambda: "test connection"

    # connectメソッドが"test connection"を返すことを確認する
    assert db.connect() == "test connection"
```

## CLI のテスト方法
### Typerのテストインターフェイスを使う

+ Typer が提供するCliRunnerを使うと、CLIのテストを容易に書くことができる。
+ [Testing - Typer](https://typer.tiangolo.com/tutorial/testing/#import-and-create-a-clirunner)
+ 以下は、myapp という名前のアプリケーションで、my_command という名前のコマンドをテストする例
    ```python 
    from typer.testing import CliRunner
    from myapp import app

    def test_my_command():
        # runner オブジェクト作成
        runner = CliRunner() 
        # invoke メソッドで、呼び出すアプリケーションとコマンドをリストで渡す
        result = runner.invoke(app, ["my_command", "--name", "John"])
        # exit_code プロパティが正常終了（０）かテスト
        assert result.exit_code == 0
        # stdout プロパティで、正しい出力かどうかテスト
        assert "Hello, John" in result.stdout
    ```

## モック作成
### 属性をモックする
+ モックとは、実際の振る舞い／動作をsimulateするもの
+ 以下は、some_function() 関数の呼び出しをモックしている。実際の関数は４２を返すが、モック化して返る値を２４に変更し、テストでは２４が返ることを確認している。テストするのは関数の「振る舞い」であって、実際の実装（return 42）ではないときに使う
    ```python 
    from unittest.mock import patch

    def some_function():
        return 42

    def test_some_function():
        with patch('__main__.some_function') as mock_function:
            mock_function.return_value = 24
            result = some_function()
        assert result == 24

    ```
+ モックは unittest.mock.patch メソッドを使って、（主に）コンテキストマネージャとして使う
+ return_value 属性を使って特定の値を返すことができる

### クラスやメソッドをモックする
1. テスト関数の中で、テスト対象のクラスをインスタンス化する
1. patch.object() メソッドをコンテキストマネージャとして使って MyClass の my_method() メソッドをモック。その時、return_valueオプションでモック用の値を指定
1. その中で、my_instance.my_method()を呼び出す
+ このような手順を踏むと、3番目の呼び出しはモック実装が呼び出される
    ```python
    from unittest.mock import patch

    class MyClass:
        def my_method(self):
            return "real implementation"

    def test_mock_class_method():
        my_instance = MyClass()
        with patch.object(MyClass, "my_method", return_value="mocked implementation"):
            result = my_instance.my_method()
        assert result == "mocked implementation"

    ```
+ 教科書の例のようにコンテキストマネージャのオブジェクトの属性を書き換える方法もある。
+ モックしたい値が、メソッドの属性の場合、`MockCardsDB.return_value.path.return_value` このように書くことができる
```python
def test_mock_path():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        MockCardsDB.return_value.path.return_value = "/foo/"
        with cards.cli.cards_db() as db:
            print()
            print(f"{db.path=}")
            print(f"{db.path()=}")

```

### autospec=True を使ってモック対象のオブジェクトのクラスや属性などの情報を自動的に取得
+ autospec=Trueを使うと、モック対象のオブジェクトが正しいメソッドや属性を持っているか検証できる
+ 以下の例は、MyClass が my_method を持っていることを自動検証している
```python 
class MyClass:
    def my_method(self):
        pass

def my_function():
    obj = MyClass()
    obj.my_method()

from unittest.mock import patch

def test_my_function():
    with patch('__main__.MyClass', autospec=True) as mock_class:
        my_function()
        mock_class.assert_called_once() 
        mock_class.return_value.my_method.assert_called_once()
    
```
+ assert_called_once() はオブジェクトが一度だけ呼び出されたことを検証する。呼び出されていなかったり、複数回呼び出された場合はテストが失敗する。

### モックオブジェクトが呼び出されたことを検証する
+ 上記で使ったassert_called_once() メソッドのように、モックの値のテストではなく、呼び出しされたかどうかをテストするメソッドが提供されている
+ assert_called()、assert_called_with()、assert_not_called() など

## 正しい例外を発生させるかテストする
+ モックオブジェクトが呼び出されたとき、実行される関数や例外を指定するための属性 side_effect を使う
+ 例：mock_obj は呼び出されると、ValueErrorが呼び出されるように、side_effect に指定
+ 例外が発生すると、 pytest がキャッチしてくれて正しい例外が発生しているかテスト
```python
from unittest.mock import Mock

def test_my_function():
    mock_obj = Mock()
    mock_obj.side_effect = ValueError("Invalid value")
    with pytest.raises(ValueError):
        my_function(mock_obj)

```
+ 具体例
+ ゼロで割り算するとValueErrorを出す divide 関数を用意
+ 同じエラーを返すオブジェクト mock を用意
+ pytest.raises に渡して、エラーのテスト
```python
import pytest
from unittest.mock import Mock

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    mock = Mock()
    mock.side_effect = ValueError("Cannot divide by zero")
    with pytest.raises(ValueError):
        divide(10, mock)

```