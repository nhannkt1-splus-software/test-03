import pytest
from datetime import datetime

# --- テスト用ダミーTicketクラス ---
class DummyTicket:
    def __init__(self, status, due_at):
        self.status = status
        self.due_at = due_at

# --- TERMINAL_STATUSESの定義 ---
TERMINAL_STATUSES = {'closed', 'resolved'}

# --- is_overdue関数のインポート ---
# テスト対象関数が同じモジュールにある場合は以下のようにインポート
# from <対象モジュール> import is_overdue

# --- utc_nowのモック用パッチ ---
import sys

@pytest.fixture(autouse=True)
def patch_globals(monkeypatch):
    # is_overdueがグローバルから参照するTERMINAL_STATUSESとutc_nowをパッチ
    monkeypatch.setitem(sys.modules[__name__].__dict__, 'TERMINAL_STATUSES', TERMINAL_STATUSES)
    yield

# --- is_overdueのutc_nowをモックするヘルパー ---
def patch_utc_now(monkeypatch, return_value=None, side_effect=None):
    def _utc_now():
        if side_effect:
            raise side_effect
        return return_value
    monkeypatch.setitem(sys.modules[__name__].__dict__, 'utc_now', _utc_now)

# --- テストケース ---
# TC1: statusがTERMINAL_STATUSESに含まれず、due_atが過去日時の場合、期限切れと判定される
def test_TC1(monkeypatch):
    # TC1
    patch_utc_now(monkeypatch, return_value=datetime(2024, 6, 2, 12, 0, 0))
    ticket = DummyTicket('open', datetime(2024, 6, 1, 12, 0, 0))
    assert is_overdue(ticket) is True

# TC2: statusがTERMINAL_STATUSESに含まれず、due_atが未来日時の場合、期限切れでないと判定される
def test_TC2(monkeypatch):
    # TC2
    patch_utc_now(monkeypatch, return_value=datetime(2024, 6, 1, 12, 0, 0))
    ticket = DummyTicket('open', datetime(2099, 1, 1, 12, 0, 0))
    assert is_overdue(ticket) is False

# TC3: statusがTERMINAL_STATUSESに含まれる場合、期限切れ判定は常にFalse
def test_TC3(monkeypatch):
    # TC3
    patch_utc_now(monkeypatch, return_value=datetime(2024, 6, 2, 12, 0, 0))
    ticket = DummyTicket('closed', datetime(2024, 6, 1, 12, 0, 0))
    assert is_overdue(ticket) is False

# TC4: due_atがNoneの場合、期限切れ判定は常にFalse
def test_TC4(monkeypatch):
    # TC4
    patch_utc_now(monkeypatch, return_value=datetime(2024, 6, 2, 12, 0, 0))
    ticket = DummyTicket('open', None)
    assert is_overdue(ticket) is False

# TC5: nowを明示的に指定し、期限切れとなるケース
def test_TC5():
    # TC5
    ticket = DummyTicket('open', datetime(2024, 6, 1, 12, 0, 0))
    now = datetime(2024, 6, 2, 12, 0, 0)
    assert is_overdue(ticket, now) is True

# TC6: nowを明示的に指定し、期限切れでないケース
def test_TC6():
    # TC6
    ticket = DummyTicket('open', datetime(2024, 6, 1, 12, 0, 0))
    now = datetime(2024, 5, 31, 12, 0, 0)
    assert is_overdue(ticket, now) is False

# TC7: ticketがNoneの場合、属性アクセスでAttributeErrorが発生
def test_TC7():
    # TC7
    with pytest.raises(AttributeError):
        is_overdue(None)

# TC8: ticketがstr型の場合、属性アクセスでAttributeErrorが発生
def test_TC8():
    # TC8
    with pytest.raises(AttributeError):
        is_overdue("invalid_type")

# TC9: due_at属性が存在しない場合、AttributeErrorが発生
class DictTicket(dict):
    # dict型で属性アクセスをサポートしない
    pass

def test_TC9():
    # TC9
    ticket = DictTicket(status='open')
    with pytest.raises(AttributeError):
        is_overdue(ticket)

# TC10: due_atがdatetime型でない場合、比較演算でTypeErrorが発生
def test_TC10():
    # TC10
    ticket = DummyTicket('open', 'not_a_datetime')
    with pytest.raises(TypeError):
        is_overdue(ticket)

# TC11: nowとdue_atが同じ場合、期限切れでないと判定される
def test_TC11():
    # TC11
    ticket = DummyTicket('open', datetime(2024, 6, 2, 12, 0, 0))
    now = datetime(2024, 6, 2, 12, 0, 0)
    assert is_overdue(ticket, now) is False

# TC12: nowがdue_atより1秒後の場合、期限切れと判定される
def test_TC12():
    # TC12
    ticket = DummyTicket('open', datetime(2024, 6, 2, 12, 0, 0))
    now = datetime(2024, 6, 2, 12, 0, 1)
    assert is_overdue(ticket, now) is True

# TC13: nowがdue_atより1秒前の場合、期限切れでないと判定される
def test_TC13():
    # TC13
    ticket = DummyTicket('open', datetime(2024, 6, 2, 12, 0, 0))
    now = datetime(2024, 6, 2, 11, 59, 59)
    assert is_overdue(ticket, now) is False

# TC14: utc_now()の呼び出しで例外が発生した場合
def test_TC14(monkeypatch):
    # TC14
    patch_utc_now(monkeypatch, side_effect=Exception("utc_now error"))
    ticket = DummyTicket('open', datetime(2024, 6, 1, 12, 0, 0))
    with pytest.raises(Exception):
        is_overdue(ticket)

# TC15: statusがTERMINAL_STATUSESに含まれる別の値の場合、期限切れ判定は常にFalse
def test_TC15(monkeypatch):
    # TC15
    patch_utc_now(monkeypatch, return_value=datetime(2024, 6, 2, 12, 0, 0))
    ticket = DummyTicket('resolved', datetime(2024, 6, 1, 12, 0, 0))
    assert is_overdue(ticket) is False

# TC16: nowが極端な未来日時の場合でも期限切れと判定される
def test_TC16():
    # TC16
    ticket = DummyTicket('open', datetime(2024, 6, 1, 12, 0, 0))
    now = datetime(2099, 1, 1, 12, 0, 0)
    assert is_overdue(ticket, now) is True

# TC17: due_atが極端な未来日時の場合、期限切れでないと判定される
def test_TC17():
    # TC17
    ticket = DummyTicket('open', datetime(2099, 1, 1, 12, 0, 0))
    now = datetime(2024, 6, 1, 12, 0, 0)
    assert is_overdue(ticket, now) is False

# TC18: utc_now()の呼び出しでTypeErrorが発生した場合
def test_TC18(monkeypatch):
    # TC18
    patch_utc_now(monkeypatch, side_effect=TypeError("utc_now type error"))
    ticket = DummyTicket('open', datetime(2024, 6, 1, 12, 0, 0))
    with pytest.raises(TypeError):
        is_overdue(ticket)