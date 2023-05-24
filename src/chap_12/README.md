# chapter 12 memo

## script と application のテスト

1. pytest
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

$ pytest 
======================================================================================================================== test session starts ========================================================================================================================
platform linux -- Python 3.8.5, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/taro/workspace/github/finpy/note-for-pytest/src/chap_12/scripts
plugins: Faker-18.5.1
collected 1 item                                                                                                                                                                                                                                                    

test_hello.py .                                                                                                                                                                                                                                               [100%]

========================================================================================================================= 1 passed in 0.09s =========================================================================================================================



1. tox




### skipdist = true

### capsys

### pythonpath = src 
