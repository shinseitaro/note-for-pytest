from pathlib import Path
from tempfile import TemporaryDirectory


def hello():
    with open("hello.txt", "w") as f:
        f.write("Hello World!\n")


# 1 （こういう事言ってるのかな？）
def test_with_no_fixture():
    hello()
    with open("hello.txt") as f:
        txt = f.read()

    assert txt == "Hello World!\n"


# 1 (TemporaryDirectoryを使ってみたかったので書いただけ)
def test_with_no_fixture1():
    with TemporaryDirectory() as td:
        s = "Hello World!"
        mypath = Path(td)
        fpath = mypath / "hello.txt"
        fpath.write_text(s)

        txt = fpath.read_text()
        assert txt == s

