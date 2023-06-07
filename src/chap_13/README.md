# chapter 13 memo

## 前準備
pyproject.toml の `[project.optional-dependencies]` に定義されている依存関係も含めてインストール
```
pip install -e "./cards_proj/[test]"
``` 

## テスト

```bash
pytest --tb=no # トレースバック無し

FAILED tests/api/test_list_done.py::test_list_done - TypeError: object of type 'NoneType' has no len()
FAILED tests/cli/test_done.py::test_done - AssertionError: assert '' == '\n  ID   sta...      a third'

```
2つ失敗する


## フラグ色々

あとで

## 前回失敗したテストだけを実行

どうやって覚えてるんだろう？

```bash 
pytest --lf --tb=no

============================================================================= test session starts ==============================================================================
platform linux -- Python 3.8.3, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/shinseitaro/workspace/github/finpy/note-for-pytest/code/ch13/cards_proj
configfile: pytest.ini
testpaths: tests
plugins: Faker-18.10.1, cov-4.1.0
collected 27 items / 25 deselected / 2 selected                                                                                                                                
run-last-failure: rerun previous 2 failures (skipped 13 files)

tests/api/test_list_done.py F                                                                                                                                            [ 50%]
tests/cli/test_done.py F                                                                                                                                                 [100%]

FAILED tests/api/test_list_done.py::test_list_done - TypeError: object of type 'NoneType' has no len()
FAILED tests/cli/test_done.py::test_done - AssertionError: assert '' == '\n  ID   sta...      a third'

```

+ 前回失敗したものだけ、ただし失敗したらそこで止める

```bash 
pytest --lf -x
```

+ `-l` ローカル変数を表示
```bash 
pytest --lf -x -l --tb=short

E   TypeError: object of type 'NoneType' has no len()
        cards_db   = <cards.api.CardsDB object at 0x7f9446632130>
        the_list   = None
```

## pdb を使う

```bash 
pytest --lf --trace

.
.
.
test_list_done.py(6)test_list_done()
-> cards_db.finish(3)
(Pdb) 

```
色々コマンドがある。

```bash 
# 現在の関数を確認
(Pdb) ll ## 現在の関数のソースを表示
  4     @pytest.mark.num_cards(10)
  5     def test_list_done(cards_db):
  6  ->     cards_db.finish(3)
  7         cards_db.finish(5)
  8  
  9         the_list = cards_db.list_done_cards()
 10  
 11         assert len(the_list) == 2
 12         for card in the_list:
 13             assert card.id in (3, 5)
 14             assert card.state == "done"
(Pdb) 
```

`list_done_cards` でコケているので、その前の行で止める

```bash 
(Pdb) until 8
> code/ch13/cards_proj/tests/api/test_list_done.py(9)test_list_done()
-> the_list = cards_db.list_done_cards()
```

`step` 

```bash 
(Pdb) step
--Call--
> code/ch13/cards_proj/src/cards/api.py(91)list_done_cards()
-> def list_done_cards(self):
```

もう一度 ll 

```bash 
(Pdb) ll
 91  ->     def list_done_cards(self):
 92             """Return the 'done' cards."""
 93             done_cards = self.list_cards(state="done")
```

ここから制御が戻るところまで実行

```bash 
(Pdb) return
--Return--
> code/ch13/cards_proj/src/cards/api.py(93)list_done_cards()->None
-> done_cards = self.list_cards(state="done")
```

`done_cards` の値を pp を使って確認

```bash 
(Pdb) pp done_cards
[Card(summary='Line for PM identify decade.', owner='Russell', state='done', id=3),
 Card(summary='Director baby season industry the describe.', owner='Cody', state='done', id=5)]
```

step 

```bash 
(Pdb) step
> code/ch13/cards_proj/tests/api/test_list_done.py(11)test_list_done()
-> assert len(the_list) == 2
```

ll

```bash 
(Pdb) ll
  4     @pytest.mark.num_cards(10)
  5     def test_list_done(cards_db):
  6         cards_db.finish(3)
  7         cards_db.finish(5)
  8  
  9         the_list = cards_db.list_done_cards()
 10  
 11  ->     assert len(the_list) == 2
 12         for card in the_list:
 13             assert card.id in (3, 5)
 14             assert card.state == "done"
```

```bash 
(Pdb) pp the_list
None
```
return 文が無いことがわかりました。

exit でpdbを終わる

```bash 
(Pdb) exit
```

## pdb & tox 

`code/ch13/cards_proj/tox.ini` に設定済み

テストが失敗したところからデバッガを開始する

```bash 
❯ tox -e py38 -- --pdb --no-cov
.pkg: _optional_hooks> python ./code/ch13/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
.pkg: get_requires_for_build_sdist> python ./code/ch13/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
.pkg: build_sdist> python ./code/ch13/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True flit_core.buildapi
py38: install_package> python -I -m pip install --force-reinstall --no-deps ./code/ch13/cards_proj/.tox/.tmp/package/2/cards-1.0.0.dev1.tar.gz
py38: commands[0]> pytest --cov=cards --cov=tests --cov-fail-under=100 --pdb --no-cov
================================ test session starts ================================
platform linux -- Python 3.8.3, pytest-7.3.1, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: ./code/ch13/cards_proj
configfile: pytest.ini
testpaths: tests
plugins: Faker-18.10.1, cov-4.1.0
collected 53 items                                                                  

tests/api/test_add.py .....                                                   [  9%]
tests/api/test_config.py .                                                    [ 11%]
tests/api/test_count.py ...                                                   [ 16%]
tests/api/test_delete.py ...                                                  [ 22%]
tests/api/test_finish.py ....                                                 [ 30%]
tests/api/test_list.py .........                                              [ 47%]
tests/api/test_list_done.py .                                                 [ 49%]
tests/api/test_start.py ....                                                  [ 56%]
tests/api/test_update.py ....                                                 [ 64%]
tests/api/test_version.py .                                                   [ 66%]
tests/cli/test_add.py ..                                                      [ 69%]
tests/cli/test_config.py ..                                                   [ 73%]
tests/cli/test_count.py .                                                     [ 75%]
tests/cli/test_delete.py .                                                    [ 77%]
tests/cli/test_done.py F
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

cards_db = <cards.api.CardsDB object at 0x7f72c2271850>
cards_cli = <function cards_cli_no_redirect.<locals>.run_cli at 0x7f72c2a4d8b0>

    def test_done(cards_db, cards_cli):
        cards_db.add_card(cards.Card("some task", state="done"))
        cards_db.add_card(cards.Card("another"))
        cards_db.add_card(cards.Card("a third", state="done"))
        output = cards_cli("done")
>       assert output == expected
E       AssertionError: assert '            ...      a third' == '\n  ID   sta...      a third'
E         - 
E         +                                   
E             ID   state   owner   summary    
E            ──────────────────────────────── 
E             1    done            some task  
E             3    done            a third

tests/cli/test_done.py:16: AssertionError
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

>>>>>>>>>>>>>>>>>>>>> PDB post_mortem (IO-capturing turned off) >>>>>>>>>>>>>>>>>>>>>
> ./code/ch13/cards_proj/tests/cli/test_done.py(16)test_done()
-> assert output == expected
(Pdb) 
```

`output` と `expected` の中身を確認

```bash 
(Pdb) pp output
('                                  \n'
 '  ID   state   owner   summary    \n'
 ' ──────────────────────────────── \n'
 '  1    done            some task  \n'
 '  3    done            a third')
(Pdb) pp expected
('\n'
 '  ID   state   owner   summary    \n'
 ' ──────────────────────────────── \n'
 '  1    done            some task  \n'
 '  3    done            a third')
(Pdb) 
```







