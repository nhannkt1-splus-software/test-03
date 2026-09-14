import pytest

# DeskErrorクラスが未定義の場合、テスト用にダミーを定義
class DeskError(Exception):
    pass

# テスト対象クラスのインポートまたは定義
from types import SimpleNamespace

# InvalidStatusTransitionクラスの定義（テスト対象）
class InvalidStatusTransition(DeskError):
    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Cannot move ticket from {current} to {target}")

# --- 正常系テスト ---
# TC1: current="open", target="closed"
def test_TC1_valid_status_strings():
    # TC1
    e = InvalidStatusTransition("open", "closed")
    assert e.current == "open"  # TC1
    assert e.target == "closed"  # TC1
    assert str(e) == "Cannot move ticket from open to closed"  # TC1

# TC2: current="pending", target="resolved"
def test_TC2_valid_status_strings():
    # TC2
    e = InvalidStatusTransition("pending", "resolved")
    assert e.current == "pending"  # TC2
    assert e.target == "resolved"  # TC2
    assert str(e) == "Cannot move ticket from pending to resolved"  # TC2

# TC3: current="", target="open"
def test_TC3_current_empty_string():
    # TC3
    e = InvalidStatusTransition("", "open")
    assert e.current == ""  # TC3
    assert e.target == "open"  # TC3
    assert str(e) == "Cannot move ticket from  to open"  # TC3

# TC4: current="open", target=""
def test_TC4_target_empty_string():
    # TC4
    e = InvalidStatusTransition("open", "")
    assert e.current == "open"  # TC4
    assert e.target == ""  # TC4
    assert str(e) == "Cannot move ticket from open to "  # TC4

# TC5: current="OPEN", target="closed"
def test_TC5_current_uppercase():
    # TC5
    e = InvalidStatusTransition("OPEN", "closed")
    assert e.current == "OPEN"  # TC5
    assert e.target == "closed"  # TC5
    assert str(e) == "Cannot move ticket from OPEN to closed"  # TC5

# TC6: current="open", target="CLOSED"
def test_TC6_target_uppercase():
    # TC6
    e = InvalidStatusTransition("open", "CLOSED")
    assert e.current == "open"  # TC6
    assert e.target == "CLOSED"  # TC6
    assert str(e) == "Cannot move ticket from open to CLOSED"  # TC6

# TC7: current="123", target="open"
def test_TC7_current_numeric_string():
    # TC7
    e = InvalidStatusTransition("123", "open")
    assert e.current == "123"  # TC7
    assert e.target == "open"  # TC7
    assert str(e) == "Cannot move ticket from 123 to open"  # TC7

# TC8: current="open", target="123"
def test_TC8_target_numeric_string():
    # TC8
    e = InvalidStatusTransition("open", "123")
    assert e.current == "open"  # TC8
    assert e.target == "123"  # TC8
    assert str(e) == "Cannot move ticket from open to 123"  # TC8

# TC17: current="closed", target="closed"
def test_TC17_same_status():
    # TC17
    e = InvalidStatusTransition("closed", "closed")
    assert e.current == "closed"  # TC17
    assert e.target == "closed"  # TC17
    assert str(e) == "Cannot move ticket from closed to closed"  # TC17

# TC18: current="resolved", target="pending"
def test_TC18_reverse_status():
    # TC18
    e = InvalidStatusTransition("resolved", "pending")
    assert e.current == "resolved"  # TC18
    assert e.target == "pending"  # TC18
    assert str(e) == "Cannot move ticket from resolved to pending"  # TC18

# TC19: current="", target=""
def test_TC19_both_empty_string():
    # TC19
    e = InvalidStatusTransition("", "")
    assert e.current == ""  # TC19
    assert e.target == ""  # TC19
    assert str(e) == "Cannot move ticket from  to "  # TC19

# TC20: current="OPEN", target="OPEN"
def test_TC20_both_uppercase():
    # TC20
    e = InvalidStatusTransition("OPEN", "OPEN")
    assert e.current == "OPEN"  # TC20
    assert e.target == "OPEN"  # TC20
    assert str(e) == "Cannot move ticket from OPEN to OPEN"  # TC20

# TC21: current="123", target="123"
def test_TC21_both_numeric_string():
    # TC21
    e = InvalidStatusTransition("123", "123")
    assert e.current == "123"  # TC21
    assert e.target == "123"  # TC21
    assert str(e) == "Cannot move ticket from 123 to 123"  # TC21

# --- 異常系テスト ---
# TC9: current=None, target="open"
def test_TC9_current_none():
    # TC9
    with pytest.raises(TypeError):  # TC9
        InvalidStatusTransition(None, "open")

# TC10: current="open", target=None
def test_TC10_target_none():
    # TC10
    with pytest.raises(TypeError):  # TC10
        InvalidStatusTransition("open", None)

# TC11: current=123, target="open"
def test_TC11_current_int():
    # TC11
    with pytest.raises(TypeError):  # TC11
        InvalidStatusTransition(123, "open")

# TC12: current="open", target=123
def test_TC12_target_int():
    # TC12
    with pytest.raises(TypeError):  # TC12
        InvalidStatusTransition("open", 123)

# TC13: current=[], target="open"
def test_TC13_current_list():
    # TC13
    with pytest.raises(TypeError):  # TC13
        InvalidStatusTransition([], "open")

# TC14: current="open", target=[]
def test_TC14_target_list():
    # TC14
    with pytest.raises(TypeError):  # TC14
        InvalidStatusTransition("open", [])

# TC15: current={}, target="open"
def test_TC15_current_dict():
    # TC15
    with pytest.raises(TypeError):  # TC15
        InvalidStatusTransition({}, "open")

# TC16: current="open", target={}
def test_TC16_target_dict():
    # TC16
    with pytest.raises(TypeError):  # TC16
        InvalidStatusTransition("open", {})