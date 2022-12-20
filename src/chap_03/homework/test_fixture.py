import pytest


# 2
@pytest.fixture()
def a_data():
    return "hoge"


@pytest.fixture()
def b_data():
    return 123


@pytest.fixture()
def c_data():
    return list("abc")


# 3
def test_a_data(a_data):
    assert a_data == "hoge"


def test_b_data(b_data):
    assert b_data == 123


# 4
def test_same_data_1(c_data):
    assert c_data == ["a", "b", "c"]


def test_same_data_2(c_data):
    assert c_data == ["a", "b", "c"]


# 5
"""
> pytest test_fixture.py --setup-show
===== test session starts =====

test_fixture.py 
        SETUP    F a_data
        test_fixture.py::test_a_data (fixtures used: a_data).
        TEARDOWN F a_data
        SETUP    F b_data
        test_fixture.py::test_b_data (fixtures used: b_data).
        TEARDOWN F b_data
        SETUP    F c_data
        test_fixture.py::test_same_data_1 (fixtures used: c_data).
        TEARDOWN F c_data
        SETUP    F c_data
        test_fixture.py::test_same_data_2 (fixtures used: c_data).
        TEARDOWN F c_data

====== 4 passed in 0.01s ======


"""

# 6
@pytest.fixture(scope="module")
def c_data_2():
    return list("abc")


def test_same_data_3(c_data_2):
    assert c_data_2 == ["a", "b", "c"]


def test_same_data_4(c_data_2):
    assert c_data_2 == ["a", "b", "c"]


# 7
"""
❯ pytest test_fixture.py --setup-show
===== test session starts =====
platform linux -- Python 3.8.3, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/shinseitaro/workspace/github/finpy/note-for-pytest/src/chap_03/homework
collected 6 items                                                                                                                   

test_fixture.py 
        SETUP    F a_data
        test_fixture.py::test_a_data (fixtures used: a_data).
        TEARDOWN F a_data
        SETUP    F b_data
        test_fixture.py::test_b_data (fixtures used: b_data).
        TEARDOWN F b_data
        SETUP    F c_data
        test_fixture.py::test_same_data_1 (fixtures used: c_data).
        TEARDOWN F c_data
        SETUP    F c_data
        test_fixture.py::test_same_data_2 (fixtures used: c_data).
        TEARDOWN F c_data
    SETUP    M c_data_2
        test_fixture.py::test_same_data_3 (fixtures used: c_data_2).
        test_fixture.py::test_same_data_4 (fixtures used: c_data_2).
    TEARDOWN M c_data_2

====== 6 passed in 0.01s ======
"""

# 8
@pytest.fixture(scope="module")
def c_data_4():
    """
    #12 これはDocStringです
    """
    # 9
    print("c_data_3 はじめ")
    yield list("abc")
    print("c_data_3 終わり")


def test_same_data_5(c_data_4):
    assert c_data_4 == ["a", "b", "c"]


def test_same_data_6(c_data_4):
    assert c_data_4 == ["a", "b", "c"]


# 10
"""
> pytest test_fixture.py -s -v
===== test session starts =====
platform linux -- Python 3.8.3, pytest-7.2.0, pluggy-1.0.0 -- /home/shinseitaro/workspace/github/finpy/note-for-pytest/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/shinseitaro/workspace/github/finpy/note-for-pytest/src/chap_03/homework
collected 8 items                                                                                                                   

test_fixture.py::test_a_data PASSED
test_fixture.py::test_b_data PASSED
test_fixture.py::test_same_data_1 PASSED
test_fixture.py::test_same_data_2 PASSED
test_fixture.py::test_same_data_3 PASSED
test_fixture.py::test_same_data_4 PASSED
test_fixture.py::test_same_data_5 c_data_3 はじめ
PASSED
test_fixture.py::test_same_data_6 PASSEDc_data_3 終わり


====== 8 passed in 0.01s ======

"""

# 11
"""
---------- fixtures defined from test_fixture -----------
c_data_4 [module scope] -- test_fixture.py:107
    no docstring available

b_data -- test_fixture.py:11
    no docstring available

c_data -- test_fixture.py:16
    no docstring available

a_data -- test_fixture.py:6
    no docstring available

c_data_2 [module scope] -- test_fixture.py:64
    no docstring available
"""

# 12
"""
--------- fixtures defined from test_fixture ----------
c_data_4 [module scope] -- test_fixture.py:107
    #12 これはDocStringです

b_data -- test_fixture.py:11
    no docstring available

c_data -- test_fixture.py:16
    no docstring available

a_data -- test_fixture.py:6
    no docstring available

c_data_2 [module scope] -- test_fixture.py:64
    no docstring available

"""

