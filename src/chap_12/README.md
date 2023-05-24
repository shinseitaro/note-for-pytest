# chapter 12 memo

## script と application のテスト

- script と test script 
    ```python
    # hello.py
    print("Hello World!")
    ```
    ```python 
    from subprocess import run 

    def test_hello():
        result = run(
            ["python", "hello.py"],
            capture_output=True, 
            text=True
        )
        output = result.stdout
        assert output == "Hello World!\n"

    ```
    - https://docs.python.org/ja/3/library/subprocess.html#subprocess.run
    - capture_output を true に設定すると、stdout および stderr が捕捉
    - text 引数が true である場合、stdin, stdout および stderr のためのファイルオブジェクトはテキストモードで返る

1. pytestでテスト実行
    ```bash 
    $ pytest 
    ====== test session starts ======
    platform linux -- Python 3.8.5, pytest-7.3.1, pluggy-1.0.0
    rootdir: /note-for-pytest/src/chap_12/scripts
    plugins: Faker-18.5.1
    collected 1 item                                                                                                                                                                                                                                                    

    test_hello.py .    [100%]

    ======= 1 passed in 0.09s =======
    ```
1. toxでテスト実行
    - 本には `skipsdist = true ` が無いとビルドエラーを起こすと書いてあったが、私の環境ではあってもなくても動いた。
    - 環境
        ```bash 
        Python 3.8.3
        pytest==7.3.1
        tox==4.5.1
        ```
    + tox.ini
        ```ini 
        [tox]
        envlist = py38
        ; skipsdist = true 

        [testenv]
        deps = pytest 
        commands = pytest 

        [pytest]
        ```
    + 結果
        ```bash 
        > tox
        py38: commands[0]> pytest
        ====== test session starts =======
        platform linux -- Python 3.8.3, pytest-7.3.1, pluggy-1.0.0
        cachedir: .tox/py38/.pytest_cache
        rootdir: /note-for-pytest/src/chap_12/scripts
        configfile: tox.ini
        collected 1 item                                                                                                                                                                 

        test_hello.py .     [100%]

        ======= 1 passed in 0.02s ========
        py38: OK (0.22=setup[0.03]+cmd[0.19] seconds)
        congratulations :) (0.27 seconds)
        ```

### script をインポートしてテスト
+ script
    ```python 
    def main():
        print("Hello World!")

    if __name__ == "__main__":
        main()
    ```
+  組み込みフィクスチャ capsys
    + capsysの詳細は [第四章](../chap_04/README.md)。ざっくりいうと
        1. stdout / stderr をキャプチャ
        1. 出力キャプチャを一時的に無効にする
    + https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html
    ```python 
    import hello

    def test_main(capsys):
        hello.main()
        output = capsys.readouterr().out
        assert output == "Hello World!\n"

    ```


### src と test ディレクトリに分かれている場合
+ script と test script 
    ```bash
    mydir
    ├── pytest.ini
    ├── src
    │   └── hello.py
    └── tests
        └── test_hello.py
    ```
    ```python 
    # hello.py
    def main():
        print("Hello World!")

    if __name__ == "__main__":
        main()
    ```
    ```python 
    # test_hello.py
    import hello

    def test_main(capsys):
        hello.main()
        output = capsys.readouterr().out
        assert output == "Hello World!\n"
    ```
    + この書き方だと普通に `python test_hello.py` しても `ModuleNotFoundError: No module named 'hello'` でコケる（当たり前）が、このままで大丈夫
+ pytest.ini に src と test パスを指定
    ```ini
    [pytest]
    addopts = -ra 
    testpaths = tests ;; ← 
    pythonpath = src ;; ←
    ```
+ 実行
    ```bash 
    > pytest 
    ===== test session starts =====
    platform linux -- Python 3.8.3, pytest-7.2.0, pluggy-1.0.0
    rootdir: /note-for-pytest/src/chap_12/mydir, configfile: pytest.ini, testpaths: tests
    plugins: Faker-17.0.0, anyio-3.6.2
    collected 1 item                                                                                                                                                                                        

    tests/test_hello.py .                                                                                                                                                                             [100%]

    ====== 1 passed in 0.04s ======
    ```
### tox に指定した requirements.txt を使う
+ script と test script 
    ```bash 
    app/
    ├── requirements.txt
    ├── src
    │   └── hello.py
    ├── tests
    │   └── test_hello.py
    └── tox.ini
    ```
    ```bash
    # requirements.txt
    typer==0.3.2
    ```
    ```python 
    # hello.py
    import typer
    from typing import Optional

    def full_output(name: str):
        return f"Hello {name}!"

    app = typer.Typer()

    @app.command()
    def main(name: Optional[str] = typer.Argument("World")):
        print(full_output(name))

    if __name__ == "__main__":
        app()
    ```
    + (確認) この様に実行できる
        ```bash
        > python src/hello.py 
        Hello World!

        > python src/hello.py shinseitaro
        Hello shinseitaro!
        ```
    ```python 
    # test_hello.py
    import hello
    from typer.testing import CliRunner

    def test_full_output():
        assert hello.full_output("Foo") == "Hello Foo!"

    runner = CliRunner()

    def test_hello_app_default():
        result = runner.invoke(hello.app)
        assert result.stdout == "Hello World!\n"

    def test_hello_app_taro():
        result = runner.invoke(hello.app, ["shinseitaro"])
        assert result.stdout == "Hello shinseitaro!\n"
    ```
+ tox.ini    
    ```ini
    [tox]
    envlist = py38
    skipsdist = true 

    [testenv]
    deps = pytest 
        pytest-srcpaths
        -r requirements.txt 

    [pytest]
    addopts = -ra
    testpaths = tests
    pythonpath = src 
    ```
    + depsに `-r requirements.txt` を追加。 
    + (教科書にはスペース無し `-rrequirements.txt` で記述されていたが、どちらでもテストできた)
    + スペース無しでダメな時もある（パスワードを渡す時など。スペースもパスワードと思われちゃうから）。なので、スペース無しでやったほうがいい

+ 実行
    ```bash 
    > tox
    py38: install_deps> python -I -m pip install pytest pytest-srcpaths -r requirements.txt
    py38: OK (1.71 seconds)
    congratulations :) (1.75 seconds)
    ```



