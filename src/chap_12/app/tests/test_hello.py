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
