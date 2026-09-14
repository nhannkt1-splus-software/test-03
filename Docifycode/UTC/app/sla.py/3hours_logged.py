import pytest

# --- テスト用のダミークラス定義 ---
# Worklog, Ticketクラスが未定義の場合のため、テスト用に定義
class Worklog:
    def __init__(self, hours):
        self.hours = hours

class Ticket:
    def __init__(self, worklogs):
        self.worklogs = worklogs

# --- テスト対象関数のインポート ---
# hours_logged関数が同一ファイルにある場合はそのまま利用
from __main__ import hours_logged

# --- テストケース ---

# TC1: worklogsが空リスト
def test_TC1_hours_logged_empty_worklogs():
    # TC1
    ticket = Ticket(worklogs=[])
    assert hours_logged(ticket) == 0.0

# TC2: worklogsに1件、hoursが1.0
def test_TC2_hours_logged_single_worklog_1_0():
    # TC2
    ticket = Ticket(worklogs=[Worklog(hours=1.0)])
    assert hours_logged(ticket) == 1.0

# TC3: worklogsに複数件、全てhoursが0.0
def test_TC3_hours_logged_multiple_zero_hours():
    # TC3
    ticket = Ticket(worklogs=[Worklog(hours=0.0), Worklog(hours=0.0)])
    assert hours_logged(ticket) == 0.0

# TC4: worklogsに複数件、hoursが小数
def test_TC4_hours_logged_multiple_decimal_hours():
    # TC4
    ticket = Ticket(worklogs=[Worklog(hours=1.234), Worklog(hours=2.345)])
    assert hours_logged(ticket) == 3.58

# TC5: worklogsに負の値を含む
def test_TC5_hours_logged_negative_hours():
    # TC5
    ticket = Ticket(worklogs=[Worklog(hours=-1.0), Worklog(hours=2.0)])
    assert hours_logged(ticket) == 1.0

# TC6: worklogsに非常に大きい値
def test_TC6_hours_logged_large_value():
    # TC6
    ticket = Ticket(worklogs=[Worklog(hours=1000000.0)])
    assert hours_logged(ticket) == 1000000.0

# TC7: 合計が四捨五入で0.01になるケース
def test_TC7_hours_logged_rounding_to_0_01():
    # TC7
    ticket = Ticket(worklogs=[Worklog(hours=0.005), Worklog(hours=0.005)])
    assert hours_logged(ticket) == 0.01

# TC8: 合計が四捨五入で0.0になるケース
def test_TC8_hours_logged_rounding_to_0_0():
    # TC8
    ticket = Ticket(worklogs=[Worklog(hours=0.004), Worklog(hours=0.004)])
    assert hours_logged(ticket) == 0.0

# TC9: worklogsのhoursがNone
def test_TC9_hours_logged_hours_is_none():
    # TC9
    ticket = Ticket(worklogs=[Worklog(hours=None)])
    with pytest.raises(TypeError):
        hours_logged(ticket)

# TC10: worklogsのhoursがstr型
def test_TC10_hours_logged_hours_is_str():
    # TC10
    ticket = Ticket(worklogs=[Worklog(hours='a')])
    with pytest.raises(TypeError):
        hours_logged(ticket)

# TC11: worklogsがNone
def test_TC11_hours_logged_worklogs_is_none():
    # TC11
    ticket = Ticket(worklogs=None)
    with pytest.raises(TypeError):
        hours_logged(ticket)

# TC12: ticketがNone
def test_TC12_hours_logged_ticket_is_none():
    # TC12
    with pytest.raises(AttributeError):
        hours_logged(None)

# TC13: ticketがint型
def test_TC13_hours_logged_ticket_is_int():
    # TC13
    with pytest.raises(AttributeError):
        hours_logged(123)

# TC14: ticketがstr型
def test_TC14_hours_logged_ticket_is_str():
    # TC14
    with pytest.raises(AttributeError):
        hours_logged('ticket')

# TC15: worklogsに1件、hoursが1.345
def test_TC15_hours_logged_single_worklog_rounding():
    # TC15
    ticket = Ticket(worklogs=[Worklog(hours=1.345)])
    assert hours_logged(ticket) == 1.35

# TC16: 合計が0.015で四捨五入で0.02になるケース
def test_TC16_hours_logged_sum_0_015_rounding():
    # TC16
    ticket = Ticket(worklogs=[Worklog(hours=0.005), Worklog(hours=0.005), Worklog(hours=0.005)])
    assert hours_logged(ticket) == 0.02

# TC17: 合計が0.009で四捨五入で0.01になるケース
def test_TC17_hours_logged_sum_0_009_rounding():
    # TC17
    ticket = Ticket(worklogs=[Worklog(hours=0.005), Worklog(hours=0.004)])
    assert hours_logged(ticket) == 0.01

# TC18: 合計が0.007で四捨五入で0.01になるケース
def test_TC18_hours_logged_sum_0_007_rounding():
    # TC18
    ticket = Ticket(worklogs=[Worklog(hours=0.004), Worklog(hours=0.003)])
    assert hours_logged(ticket) == 0.01

# TC19: 合計が0.002で四捨五入で0.0になるケース
def test_TC19_hours_logged_sum_0_002_rounding():
    # TC19
    ticket = Ticket(worklogs=[Worklog(hours=0.001), Worklog(hours=0.001)])
    assert hours_logged(ticket) == 0.0

# TC20: 非常に小さい値の合計
def test_TC20_hours_logged_very_small_values():
    # TC20
    ticket = Ticket(worklogs=[Worklog(hours=1e-10), Worklog(hours=1e-10)])
    assert hours_logged(ticket) == 0.0

# TC21: 正負の値で合計が0.0
def test_TC21_hours_logged_positive_and_negative_cancel():
    # TC21
    ticket = Ticket(worklogs=[Worklog(hours=1.0), Worklog(hours=-1.0)])
    assert hours_logged(ticket) == 0.0

# TC22: worklogs内のhoursが数値文字列だが型違い
def test_TC22_hours_logged_hours_is_numeric_str():
    # TC22
    ticket = Ticket(worklogs=[Worklog(hours=1.0), Worklog(hours='2.0')])
    with pytest.raises(TypeError):
        hours_logged(ticket)
```
