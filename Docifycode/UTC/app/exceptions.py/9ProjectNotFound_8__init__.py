import pytest

# テスト対象クラスのインポート
from target_module import ProjectNotFound  # 実際のモジュール名に置き換えてください

# DeskErrorが未定義の場合のためのダミークラス
class DeskError(Exception):
    pass

# --- 正常系テスト ---

# TC1: int型の正の整数
def test_TC1_int_positive():
    # テストID: TC1
    key = 1
    e = ProjectNotFound(key)
    # key属性が正しくセットされているか
    assert e.key == key
    # メッセージが正しいか
    assert str(e) == "Project 1 was not found"

# TC2: int型のゼロ
def test_TC2_int_zero():
    # テストID: TC2
    key = 0
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project 0 was not found"

# TC3: int型の負の整数
def test_TC3_int_negative():
    # テストID: TC3
    key = -1
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project -1 was not found"

# TC4: str型の英字文字列
def test_TC4_str_alpha():
    # テストID: TC4
    key = "abc"
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project abc was not found"

# TC5: str型の空文字列（境界値）
def test_TC5_str_empty():
    # テストID: TC5
    key = ""
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project  was not found"

# TC6: str型の数字文字列
def test_TC6_str_digit():
    # テストID: TC6
    key = "123"
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project 123 was not found"

# TC7: int型の非常に大きな値（境界値）
def test_TC7_int_large():
    # テストID: TC7
    key = 999999999999999999999999
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == f"Project {key} was not found"

# TC8: str型の記号文字列
def test_TC8_str_symbols():
    # テストID: TC8
    key = "!@#$%^&*()"
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project !@#$%^&*() was not found"

# TC14: str型の長い文字列（境界値テスト）
def test_TC14_str_long_100():
    # テストID: TC14
    key = "a" * 100
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == f"Project {key} was not found"

# TC15: str型の日本語文字列
def test_TC15_str_japanese():
    # テストID: TC15
    key = "\u3042\u3044\u3046\u3048\u304a"  # あいうえお
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == f"Project {key} was not found"

# TC16: str型の制御文字を含む文字列
def test_TC16_str_control_chars():
    # テストID: TC16
    key = "\n\t\r"
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == f"Project {key} was not found"

# TC17: str型の非常に長い文字列（ストレステスト）
def test_TC17_str_very_long_1000():
    # テストID: TC17
    key = "b" * 1000
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == f"Project {key} was not found"

# --- 異常系テスト ---

# TC9: NoneType（型違い）
def test_TC9_none_type():
    # テストID: TC9
    key = None
    e = ProjectNotFound(key)
    assert e.key is None
    assert str(e) == "Project None was not found"

# TC10: float型（型違い）
def test_TC10_float_type():
    # テストID: TC10
    key = 3.14
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project 3.14 was not found"

# TC11: list型（型違い）
def test_TC11_list_type():
    # テストID: TC11
    key = []
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project [] was not found"

# TC12: dict型（型違い）
def test_TC12_dict_type():
    # テストID: TC12
    key = {}
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project {} was not found"

# TC13: bool型（型違い）
def test_TC13_bool_type():
    # テストID: TC13
    key = True
    e = ProjectNotFound(key)
    assert e.key == key
    assert str(e) == "Project True was not found"