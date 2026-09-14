import pytest
import datetime
from functools import partial

# --- テスト対象のimport ---
# due_at_for, Priority, SLA_HOURS がグローバルスコープにあると仮定
# もしimportが必要なら、下記のようにimportする
# from target_module import due_at_for, Priority, SLA_HOURS

# Priority, SLA_HOURSのダミー定義（テスト環境で未定義の場合のみ有効）
try:
    Priority
except NameError:
    from enum import Enum
    class Priority(Enum):
        HIGH = 1
        NORMAL = 2
        LOW = 3
        UNKNOWN = 99
try:
    SLA_HOURS
except NameError:
    SLA_HOURS = {
        Priority.HIGH: 8,
        Priority.NORMAL: 4,
        Priority.LOW: 2,
        # Priority.UNKNOWN は含めない
    }

# --- テストケース ---

# TC1: 正常系 Priority.HIGH
def test_due_at_for_TC1():
    # TC1
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = Priority.HIGH
    expected = datetime.datetime(2024, 6, 1, 20, 0, 0)
    # 実行と検証
    assert due_at_for(created_at, priority) == expected

# TC2: 正常系 Priority.LOW
def test_due_at_for_TC2():
    # TC2
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = Priority.LOW
    expected = datetime.datetime(2024, 6, 1, 14, 0, 0)
    assert due_at_for(created_at, priority) == expected

# TC3: 正常系 Priority.NORMAL
def test_due_at_for_TC3():
    # TC3
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = Priority.NORMAL
    expected = datetime.datetime(2024, 6, 1, 16, 0, 0)
    assert due_at_for(created_at, priority) == expected

# TC4: 境界値 created_atが過去の最小値
def test_due_at_for_TC4():
    # TC4
    created_at = datetime.datetime(1970, 1, 1, 0, 0, 0)
    priority = Priority.HIGH
    expected = datetime.datetime(1970, 1, 1, 8, 0, 0)
    assert due_at_for(created_at, priority) == expected

# TC5: 境界値 created_atが未来の最大値（オーバーフローの可能性）
def test_due_at_for_TC5():
    # TC5
    created_at = datetime.datetime(9999, 12, 31, 23, 59, 59)
    priority = Priority.LOW
    # オーバーフローが発生する場合は例外になる
    try:
        expected = datetime.datetime(10000, 1, 1, 1, 59, 59)
    except ValueError:
        expected = None  # datetimeの範囲外
    if expected is not None:
        assert due_at_for(created_at, priority) == expected
    else:
        with pytest.raises(OverflowError):
            due_at_for(created_at, priority)

# TC6: 異常系 created_atがNone
def test_due_at_for_TC6():
    # TC6
    created_at = None
    priority = Priority.HIGH
    with pytest.raises(TypeError):
        due_at_for(created_at, priority)

# TC7: 異常系 created_atがint型
def test_due_at_for_TC7():
    # TC7
    created_at = 123
    priority = Priority.HIGH
    with pytest.raises(TypeError):
        due_at_for(created_at, priority)

# TC8: 異常系 created_atがstr型
def test_due_at_for_TC8():
    # TC8
    created_at = '2024-06-01T12:00:00'
    priority = Priority.HIGH
    with pytest.raises(TypeError):
        due_at_for(created_at, priority)

# TC9: 異常系 priorityがNone
def test_due_at_for_TC9():
    # TC9
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = None
    with pytest.raises(TypeError):
        due_at_for(created_at, priority)

# TC10: 異常系 priorityがint型
def test_due_at_for_TC10():
    # TC10
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = 5
    with pytest.raises(TypeError):
        due_at_for(created_at, priority)

# TC11: 異常系 priorityがstr型
def test_due_at_for_TC11():
    # TC11
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = 'HIGH'
    with pytest.raises(TypeError):
        due_at_for(created_at, priority)

# TC12: 異常系 priorityがSLA_HOURSに存在しない値
def test_due_at_for_TC12():
    # TC12
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    priority = Priority.UNKNOWN
    with pytest.raises(KeyError):
        due_at_for(created_at, priority)

# TC13: 部分適用 Priority.HIGH
def test_due_at_for_TC13():
    # TC13
    partial_func = partial(due_at_for, priority=Priority.HIGH)
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    expected = datetime.datetime(2024, 6, 1, 20, 0, 0)
    assert partial_func(created_at) == expected

# TC14: 部分適用 Priority.LOW
def test_due_at_for_TC14():
    # TC14
    partial_func = partial(due_at_for, priority=Priority.LOW)
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    expected = datetime.datetime(2024, 6, 1, 14, 0, 0)
    assert partial_func(created_at) == expected

# TC15: 部分適用 Priority.NORMAL
def test_due_at_for_TC15():
    # TC15
    partial_func = partial(due_at_for, priority=Priority.NORMAL)
    created_at = datetime.datetime(2024, 6, 1, 12, 0, 0)
    expected = datetime.datetime(2024, 6, 1, 16, 0, 0)
    assert partial_func(created_at) == expected