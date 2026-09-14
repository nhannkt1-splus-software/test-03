import pytest

# --- テスト対象クラスのインポート ---
# from <module> import LabelNotFound

# DeskErrorのダミー定義（テスト用: 本来は本体からインポートすること）
class DeskError(Exception):
    pass

# --- テスト対象クラスの再掲（テスト用: 本来は本体からインポートすること）---
class LabelNotFound(DeskError):
    def __init__(self, key: int | str) -> None:
        self.key = key
        super().__init__(f"Label {key} was not found")

# --- テストケース ---

# TC1: int型のkey（通常値）
def test_TC1_label_not_found_with_int_key():
    # TC1
    key = 1
    exc = LabelNotFound(key)
    # key属性が正しくセットされているか
    assert exc.key == key
    # メッセージが正しいか
    assert str(exc) == "Label 1 was not found"

# TC2: int型のkey（境界値: 0）
def test_TC2_label_not_found_with_int_zero():
    # TC2
    key = 0
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label 0 was not found"

# TC3: int型のkey（負の値）
def test_TC3_label_not_found_with_negative_int():
    # TC3
    key = -1
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label -1 was not found"

# TC4: int型のkey（非常に大きい値）
def test_TC4_label_not_found_with_large_int():
    # TC4
    key = 999999999
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label 999999999 was not found"

# TC5: str型のkey（英字+記号）
def test_TC5_label_not_found_with_str_key():
    # TC5
    key = "label_abc"
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label label_abc was not found"

# TC6: 空文字列のkey
def test_TC6_label_not_found_with_empty_str():
    # TC6
    key = ""
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label  was not found"

# TC7: 日本語文字列のkey
def test_TC7_label_not_found_with_japanese_str():
    # TC7
    key = "ラベル名"
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label ラベル名 was not found"

# TC8: 特殊文字を含むstr型のkey
def test_TC8_label_not_found_with_special_char_str():
    # TC8
    key = "!@#$%^&*()"
    exc = LabelNotFound(key)
    assert exc.key == key
    assert str(exc) == "Label !@#$%^&*() was not found"

# TC9: None型（型不一致）
def test_TC9_label_not_found_with_none():
    # TC9
    key = None
    with pytest.raises(TypeError):
        LabelNotFound(key)

# TC10: float型（型不一致）
def test_TC10_label_not_found_with_float():
    # TC10
    key = 0.5
    with pytest.raises(TypeError):
        LabelNotFound(key)

# TC11: list型（型不一致）
def test_TC11_label_not_found_with_list():
    # TC11
    key = []
    with pytest.raises(TypeError):
        LabelNotFound(key)

# TC12: dict型（型不一致）
def test_TC12_label_not_found_with_dict():
    # TC12
    key = {}
    with pytest.raises(TypeError):
        LabelNotFound(key)
```
