# chapter 08 memo

## まとめ
1. 設定ファイルは `pytest.ini`
    + `pytest.ini` 以外では、以下のいずれかのファイルが使える
        + `pypoject.toml`
        + `tox.ini`
        + `setup.config` 
    - 設定ファイルが設置されているディレクトリがルートディレクトリ(rootdir)
    - 設定には、`addopts` などのオプションやフラグも設定できる
1. `conftest.py` に記述したフィクスチャやフック関数は、設置したディレクトリ配下（サブディレクトリも含む）で共有できる
1. テストのサブディレクトリに `__init__.py` を配置すると重複する名前のファイルを使用可

## 設定ファイル
### 基本構成

```bash 
cards_proj
├── pytest.ini # pytestデフォルト設定。１プロジェクトに１つだけ設置。ここが rootdir になる。
└── tests
    ├── api
    │   ├── __init__.py # 設置しておくと同名のテストファイルを設定可
    │   ├── conftest.py 
    │   ├── sub
    │   │   └── test_sub_api.py
    │   └── test_api1.py 
    │   └── test_hoge.py # __init__.py があるのでディレクトリ違いの同名ファイルを設置可   
    ├── cli
    │   ├── __init__.py
    │   ├── conftest.py
    │   └── test_cli1.py
    │   └── test_hoge.py # 同名ファイル
    └── conftest.py # フィクスチャやフック関数設置。同列配下の全テストに有効
```
### 書き方
#### `pytest.ini`

```ini
[pytest] ; 先頭に明記

testpaths = tests ; <設定> = <値> 形式で書く

addopts = ; 複数設定の、改行書式
    --strict-markers ; 
    --strict-config
    -ra

addopts = --strict-markers --strict-config -ra ;; 一行でもOK

markers = ; マーカーは一行の１つずつ
    smoke: subset of tests
    exception: check for expected exceptions

```
- `testpaths` ：どこでテストを探せばよいかを指定
- `addopts` ：プロジェクトで常に実行したいPytestフラグを設定
    - `--strict-markers` ：登録されていないマーカーがあれば例外を出す（デフォルトは警告）
    - `--strict-config` ：設定ファイルの解析で例外があれば出す（デフォルトは警告）
    - `-ra` ：サマリーを表示（デフォルトはテストの失敗とエラーに関する情報のみ）

#### `conftest.py`
+ Chapter3参照
+ （フック関数は chapter 15）

#### `__init__.py`
+ 重複するテストファイル名を使えるようにする
+ 設定しないと、同じ名前のファイルがあるから名前変更して、というエラーメッセージが出る。

### その他の設定ファイル
#### `tox.ini`
```ini 
[tox]
; toxでの設定を書く。Chapter11に詳細あり

[pytest]
addopts =
    --strict-markers
    --strict-config
    -ra

testpaths = tests

markers =
    smoke: subset of tests
    exception: check for expected exceptions
```
#### `pypoject.toml`
```toml
[tool.pytest.ini_options] # セクション始まり
addopts = [ # リストで指定
    "--strict-markers", # 設定値は "" で囲む
    "--strict-config",
    "-ra"
    ]

testpaths = "tests"

markers = [
    "smoke: subset of tests",
    "exception: check for expected exceptions"
]

```

#### `setup.config` 
```ini 
[tool:pytest] ; ココが違うだけで後は pytest.iniと同じ
addopts =
    --strict-markers
    --strict-config
    -ra

testpaths = tests

markers =
    smoke: subset of tests
    exception: check for expected exceptions

```