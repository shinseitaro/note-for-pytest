# chapter 11 memo

## キーワード

+ CI Continuous Integration : チームで開発を行っているときに、各自が共有リポジトリにコードの変更をマージする手法
+ tox ：python のための仮想環境管理およびテストツール。バージョン管理、依存関係の解決、テスト実行、スタイルチェック、静的解析、カバレッジ測定などのタスクを実行する。異なる環境でもOK。CIプラットフォームの一部として使われることがおおい


## まなんだこと


+ tox と Github Actions を使って Python の複数バージョンでテストする
+ 複数の tox 環境を同時に実行
+ coverage を使ってテスト
+ coverage のパーセンテージを設定
+ 特定の環境を実行
+ tox CLIからPytestにパラメータを渡す
+ Github ActionsでToxを実行する

## tox 

tox の流れ

1. setup.py / pyproject.toml に格納されているプロジェクト情報を読む
1. tox.ini ファイルの作成
    + プロジェクトルートに置く
    + tox が実行するタスクやテスト環境の定義を含む
    + 同じ内容は pyproject.toml 等にも記述できるが、tox を使ってテストをする場合、tox.ini に記述されている内容が優先される
1. .tox ディレクトリに仮想環境を作成
    + 依存環境のインストール、バージョンの切り替えも行う
1. テスト実行
    + Pytest や nose を使うことができる
    + HTMLなどに出力も可
1. クリーンアップ
    + テスト完了後、仮想環境を削除
    + キャッシュのクリアなどもやってくれる

## 準備

### tox インストール

仮想環境に pip install tox 

### ディレクトリとファイル構成
```bash
cp code/cards_proj/ src/chap_11/ -r
cd src/chap_11/cards_proj

mkdir tests 
mkdir tests/api  
mkdir tests/cli 
# testファイルはcode/ch11/cards_proj/tests をコピペした

touch tox.ini

tree .
.
├── README.md
└── cards_proj
    ├── LICENSE
    ├── README.md
    ├── pyproject.toml
    ├── src
    │   └── cards
    │       ├── __init__.py
    │       ├── api.py
    │       ├── cli.py
    │       └── db.py
    ├── tests
    │   ├── api ...
    │   └── cli ...
    └── tox.ini

```
### tox 記述

```ini
[tox]
envlist = py38 
isolated_build = True ; ビルド用の仮想環境を作成してその中でビルドする。他に影響しないようにすると同時にビルドの再現性を確保

[testenv]
deps = 
    pytest
    faker
commands = pytest
```

### tox 実行

project directory で tox を実行

```bash
$ pwd 
./src/chap_11/cards_proj

$ tox
py308: install_deps> python -I -m pip install faker pytest
.pkg: install_requires> python -I -m pip install 'flit_core<4,>=3.2'
.pkg: _optional_hooks> python ./.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
.pkg: get_requires_for_build_sdist> python ./.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
.pkg: build_sdist> python ./.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
py308: install_package_deps> python -I -m pip install rich==10.7.0 tinydb==4.5.1 typer==0.3.2
py308: install_package> python -I -m pip install --force-reinstall --no-deps ./src/chap_11/cards_proj/.tox/.tmp/package/1/cards-1.0.0.tar.gz
py308: commands[0]> pytest
================ test session starts ================
platform linux -- Python 3.8.5, pytest-7.3.1, pluggy-1.0.0
cachedir: .tox/py308/.pytest_cache
rootdir: ./src/chap_11/cards_proj
plugins: Faker-18.7.0
collected 51 items                                                                                                                                                                                                  

tests/api/test_add.py .....                [  9%]
tests/api/test_config.py .                 [ 11%]
tests/api/test_count.py ...                [ 17%]
tests/api/test_delete.py ...               [ 23%]
tests/api/test_finish.py ....              [ 31%]
tests/api/test_list.py .........           [ 49%]
tests/api/test_start.py ....               [ 56%]
tests/api/test_update.py ....              [ 64%]
tests/api/test_version.py .                [ 66%]
tests/cli/test_add.py ..                   [ 70%]
tests/cli/test_config.py ..                [ 74%]
tests/cli/test_count.py .                  [ 76%]
tests/cli/test_delete.py .                 [ 78%]
tests/cli/test_errors.py .....             [ 88%]
tests/cli/test_finish.py .                 [ 90%]
tests/cli/test_list.py ..                  [ 94%]
tests/cli/test_start.py .                  [ 96%]
tests/cli/test_update.py .                 [ 98%]
tests/cli/test_version.py .                [100%]

================ warnings summary ================
tests/api/test_add.py:23
  ./src/chap_11/cards_proj/tests/api/test_add.py:23: PytestUnknownMarkWarning: Unknown pytest.mark.num_cards - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.num_cards(3)

tests/api/test_count.py:14
  ./src/chap_11/cards_proj/tests/api/test_count.py:14: PytestUnknownMarkWarning: Unknown pytest.mark.num_cards - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.num_cards(1)

tests/api/test_count.py:19
  ./src/chap_11/cards_proj/tests/api/test_count.py:19: PytestUnknownMarkWarning: Unknown pytest.mark.num_cards - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.num_cards(3)

tests/cli/test_count.py:4
  ./src/chap_11/cards_proj/tests/cli/test_count.py:4: PytestUnknownMarkWarning: Unknown pytest.mark.num_cards - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.num_cards(3)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================ 51 passed, 4 warnings in 1.36s ================
.pkg: _exit> python ./.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
  py308: OK (11.71=setup[9.54]+cmd[2.17] seconds)
  congratulations :) (11.79 seconds)
```
### 複数バージョンで実行

`tox_multi-version.ini` 作成

```ini
[tox]
envlist = py38, py37
isolated_build = True 
skip_missing_interpreters = True ; python interpreter がないときは、skip 
```

```bash
$ tox -c tox_multi-version.ini ## ini ファイルを指定して実行することもできる
....
================ 51 passed, 4 warnings in 0.40s ================
py38: OK ✔ in 2 seconds
py37: skipped because could not find python interpreter with spec(s): py37
.pkg: _exit> python ./.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
  py38: OK (2.00=setup[1.28]+cmd[0.71] seconds)
  py37: SKIP (0.21 seconds)
  congratulations :) (2.26 seconds)
....
```
+ ちゃんとスキップされた
+ ちなみにこれいつ使うの？プロジェクト用に仮想環境を作っている場合、Pythonのバージョンは1つですよね？

### 複数の tox を同時に実行
```bash 
$ tox -c tox_multi-version.ini -p
```

### カバレッジレポートを tox に追加

1. `tox_coverage.ini `
  ```ini
  [tox]
  envlist = py38
  isolated_build = True

  [testenv]
  deps = 
      pytest
      faker
      pytest-cov ; 追記
  commands = pytest --cov=cards ; 追記
  ```

1. `src/chap_11/cards_proj/.coveragerc` で、.tox 仮想環境下のどこに cards ディレクトリがあるかを教える。（テストする cards ツールは、.tox 仮想環境配下のものであるため）
  ```ini
  [paths]
  source = 
      src
      .tox/*/site-packages
  ```

```bash 
tox -c tox_coverage.ini 

...

----------- coverage: platform linux, python 3.8.3-final-0 -----------
Name                                                      Stmts   Miss  Cover
-----------------------------------------------------------------------------
.tox/py38/lib/python3.8/site-packages/cards/__init__.py       3      0   100%
.tox/py38/lib/python3.8/site-packages/cards/api.py           70      0   100%
.tox/py38/lib/python3.8/site-packages/cards/cli.py           86      0   100%
.tox/py38/lib/python3.8/site-packages/cards/db.py            23      0   100%
-----------------------------------------------------------------------------
TOTAL                                                       182      0   100%
```

### カバレッジのベースラインを指定

カバレッジのベースラインは、テストスイートによってどの程度のコードカバレッジが得られるかを示す最小値  
プロジェクトの品質を測定するための基準として使用される

```ini
...
commands = pytest --cov=cards --cov=tests --cov-fail-under=100
```

### tox から pytest にパラメータを渡す

`{posargs}` を追加すると、パラメータを渡すことができる。

```ini
...
commands =
  pytest --cov=cards --cov=tests --cov-fail-under=100 {posargs}
```

パラメータを渡す時は、 -- を追加する。

```bash
tox -c tox.ini -- -k test_version --no-cov
``` 

### Github Actions を使って tox 実行

（相談）













