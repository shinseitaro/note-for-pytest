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
## マーカーとフィクスチャ
## pytest.ini

