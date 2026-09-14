import pytest
import re

# テスト対象関数のインポート
from target_module import slugify  # 必要に応じてモジュール名を修正してください

# TC1: "hello world" # 英字と空白を含む文字列
def test_slugify_tc1():
    # 期待値: "hello-world"
    assert slugify("hello world") == "hello-world"

# TC2: "Hello World!" # 大文字と記号を含む文字列
def test_slugify_tc2():
    # 期待値: "hello-world"
    assert slugify("Hello World!") == "hello-world"

# TC3: "こんにちは" # 日本語文字列
def test_slugify_tc3():
    # 期待値: ""（非英数字は除去される）
    assert slugify("こんにちは") == ""

# TC4: "123" # 数字のみの文字列
def test_slugify_tc4():
    # 期待値: "123"
    assert slugify("123") == "123"

# TC5: "hello123" # 英字と数字の混合文字列
def test_slugify_tc5():
    # 期待値: "hello123"
    assert slugify("hello123") == "hello123"

# TC6: "hello@world.com" # 記号を含むメールアドレス形式の文字列
def test_slugify_tc6():
    # 期待値: "hello-world-com"
    assert slugify("hello@world.com") == "hello-world-com"

# TC7: "   hello   " # 前後に空白を含む文字列
def test_slugify_tc7():
    # 期待値: "hello"
    assert slugify("   hello   ") == "hello"

# TC8: "" # 空文字列
def test_slugify_tc8():
    # 期待値: ""
    assert slugify("") == ""

# TC9: "-hello-" # 前後にハイフンを含む文字列
def test_slugify_tc9():
    # 期待値: "hello"
    assert slugify("-hello-") == "hello"

# TC10: "a" # 1文字の文字列
def test_slugify_tc10():
    # 期待値: "a"
    assert slugify("a") == "a"

# TC11: "A" # 大文字1文字の文字列
def test_slugify_tc11():
    # 期待値: "a"
    assert slugify("A") == "a"

# TC12: "!@#$%^&*()" # 記号のみの文字列
def test_slugify_tc12():
    # 期待値: ""（全て除去される）
    assert slugify("!@#$%^&*()") == ""

# TC13: "a b c d e f g" # 複数単語の文字列
def test_slugify_tc13():
    # 期待値: "a-b-c-d-e-f-g"
    assert slugify("a b c d e f g") == "a-b-c-d-e-f-g"

# TC14: "a_b_c" # アンダースコアを含む文字列
def test_slugify_tc14():
    # 期待値: "a-b-c"
    assert slugify("a_b_c") == "a-b-c"

# TC15: "a--b--c" # ハイフンが連続する文字列
def test_slugify_tc15():
    # 期待値: "a-b-c"
    assert slugify("a--b--c") == "a-b-c"

# TC16: None # None型
def test_slugify_tc16():
    # 期待値: TypeError
    with pytest.raises(TypeError):
        slugify(None)

# TC17: 123 # int型
def test_slugify_tc17():
    # 期待値: TypeError
    with pytest.raises(TypeError):
        slugify(123)

# TC18: 12.34 # float型
def test_slugify_tc18():
    # 期待値: TypeError
    with pytest.raises(TypeError):
        slugify(12.34)

# TC19: ["hello", "world"] # list型
def test_slugify_tc19():
    # 期待値: TypeError
    with pytest.raises(TypeError):
        slugify(["hello", "world"])

# TC20: {"key": "value"} # dict型
def test_slugify_tc20():
    # 期待値: TypeError
    with pytest.raises(TypeError):
        slugify({"key": "value"})

# TC21: "a string with 100 characters, all lowercase letters"
def test_slugify_tc21():
    # 100文字の小文字英字
    s = "a" * 100
    # 期待値: 100文字の"a"
    assert slugify(s) == s

# TC22: "a string with 100 characters, all uppercase letters"
def test_slugify_tc22():
    # 100文字の大文字英字
    s = "A" * 100
    # 期待値: 100文字の"a"
    assert slugify(s) == "a" * 100

# TC23: "a string with 50 spaces"
def test_slugify_tc23():
    # 50個の空白
    s = " " * 50
    # 期待値: ""（全て除去される）
    assert slugify(s) == ""

# TC24: "a string with only hyphens, 20 hyphens"
def test_slugify_tc24():
    # 20個のハイフン
    s = "-" * 20
    # 期待値: ""（全て除去される）
    assert slugify(s) == ""

# TC25: "a string with only underscores, 20 underscores"
def test_slugify_tc25():
    # 20個のアンダースコア
    s = "_" * 20
    # 期待値: ""（全て除去される）
    assert slugify(s) == ""

# TC26: "a string with special characters and numbers: !@#123$%^"
def test_slugify_tc26():
    # 期待値: "123"
    assert slugify("!@#123$%^") == "123"

# TC27: "a string with mixed languages: helloこんにちはworld"
def test_slugify_tc27():
    # 期待値: "helloworld"
    assert slugify("helloこんにちはworld") == "helloworld"

# TC28: "a string with leading and trailing spaces and hyphens:   -hello-   "
def test_slugify_tc28():
    # 期待値: "hello"
    assert slugify("   -hello-   ") == "hello"

# TC29: "a string with multiple consecutive special characters: hello!!!world---test"
def test_slugify_tc29():
    # 期待値: "hello-world-test"
    assert slugify("hello!!!world---test") == "hello-world-test"

# TC30: "a string with numbers and letters separated by special characters: 123_abc-456"
def test_slugify_tc30():
    # 期待値: "123-abc-456"
    assert slugify("123_abc-456") == "123-abc-456"