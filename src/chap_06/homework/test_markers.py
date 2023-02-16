import pytest

pytestmark = pytest.mark.all


@pytest.mark.odd
def test_one():
    pass


def test_two():
    pass


@pytest.mark.odd
def test_three():
    pass


@pytest.mark.testclass
class TestClass:
    def test_four(self):
        pass

    @pytest.mark.odd
    def test_five(self):
        pass


@pytest.mark.parametrize("x", [6, pytest.param(7, marks=pytest.mark.odd)])
def test_param(x):
    pass


# 問題8
# pytest -m "odd"  -v -k test_param
# test_markers.py::test_param[7] PASSED

