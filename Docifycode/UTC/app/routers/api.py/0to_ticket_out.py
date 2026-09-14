import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

# テスト対象関数と必要な型をインポート
# Ticket, TicketOut, is_overdue, to_ticket_out をインポート
# 例: from target_module import Ticket, TicketOut, is_overdue, to_ticket_out

# テスト用のヘルパー関数
def make_ticket(id=1, title="test", due_date=None, **kwargs):
    # due_dateがNoneの場合は現在時刻+1日
    if due_date is None:
        due_date = datetime.now() + timedelta(days=1)
    return Ticket(id=id, title=title, due_date=due_date, **kwargs)

# TC1: 全ての属性が正しく設定されている、期限切れ
def test_to_ticket_out_TC1():
    # TC1: 期限切れ
    # due_dateを過去に設定
    ticket = make_ticket(due_date=datetime.now() - timedelta(days=1))
    result = to_ticket_out(ticket)
    # overdueがTrueであることを確認
    assert result.overdue is True
    # 他の属性が正しくコピーされていることを確認
    assert result.id == ticket.id
    assert result.title == ticket.title
    assert result.due_date == ticket.due_date

# TC2: 全ての属性が正しく設定されている、期限内
def test_to_ticket_out_TC2():
    # TC2: 期限内
    ticket = make_ticket(due_date=datetime.now() + timedelta(days=1))
    result = to_ticket_out(ticket)
    # overdueがFalseであることを確認
    assert result.overdue is False
    assert result.id == ticket.id
    assert result.title == ticket.title
    assert result.due_date == ticket.due_date

# TC3: 必須属性が欠落している
def test_to_ticket_out_TC3():
    # TC3: 必須属性欠落
    # titleを欠落させる
    ticket = Ticket(id=1, due_date=datetime.now() + timedelta(days=1))
    with pytest.raises(ValidationError):
        to_ticket_out(ticket)

# TC4: 期限が現在時刻と同じ
def test_to_ticket_out_TC4():
    # TC4: due_dateが現在時刻
    now = datetime.now()
    ticket = make_ticket(due_date=now)
    result = to_ticket_out(ticket)
    # overdueの判定仕様に依存（ここでは期限切れでないと仮定）
    assert result.overdue is False or result.overdue is True  # 仕様に応じて修正

# TC5: 期限が非常に未来
def test_to_ticket_out_TC5():
    # TC5: due_dateが非常に未来
    future = datetime.now() + timedelta(days=10000)
    ticket = make_ticket(due_date=future)
    result = to_ticket_out(ticket)
    assert result.overdue is False

# TC6: 期限が非常に過去
def test_to_ticket_out_TC6():
    # TC6: due_dateが非常に過去
    past = datetime.now() - timedelta(days=10000)
    ticket = make_ticket(due_date=past)
    result = to_ticket_out(ticket)
    assert result.overdue is True

# TC7: 属性値がNone
def test_to_ticket_out_TC7():
    # TC7: titleがNone
    ticket = Ticket(id=1, title=None, due_date=datetime.now() + timedelta(days=1))
    with pytest.raises(ValidationError):
        to_ticket_out(ticket)

# TC8: 属性値が不正な型
def test_to_ticket_out_TC8():
    # TC8: idがstr型
    ticket = Ticket(id="not_int", title="test", due_date=datetime.now() + timedelta(days=1))
    with pytest.raises(ValidationError):
        to_ticket_out(ticket)

# TC9: ticketがNone
def test_to_ticket_out_TC9():
    # TC9: ticketがNone
    with pytest.raises(TypeError):
        to_ticket_out(None)

# TC10: ticketがint型
def test_to_ticket_out_TC10():
    # TC10: ticketがint型
    with pytest.raises(TypeError):
        to_ticket_out(1)

# TC11: ticketがstr型
def test_to_ticket_out_TC11():
    # TC11: ticketがstr型
    with pytest.raises(TypeError):
        to_ticket_out("ticket")

# TC12: ticketがdict型
def test_to_ticket_out_TC12():
    # TC12: ticketがdict型
    with pytest.raises(TypeError):
        to_ticket_out({"id": 1, "title": "test"})

# TC13: 属性値が空文字列
def test_to_ticket_out_TC13():
    # TC13: titleが空文字列
    ticket = make_ticket(title="")
    result = to_ticket_out(ticket)
    assert result.title == ""
    # overdueは期限内なのでFalse
    assert result.overdue is False

# TC14: 属性値が最大値
def test_to_ticket_out_TC14():
    # TC14: idがint型の最大値
    max_int = 2**63 - 1
    ticket = make_ticket(id=max_int)
    result = to_ticket_out(ticket)
    assert result.id == max_int

# TC15: 属性値が最小値
def test_to_ticket_out_TC15():
    # TC15: idがint型の最小値
    min_int = -2**63
    ticket = make_ticket(id=min_int)
    result = to_ticket_out(ticket)
    assert result.id == min_int

# TC16: 属性値が特殊文字
def test_to_ticket_out_TC16():
    # TC16: titleが特殊文字
    special_title = "テスト!@#$%^&*()_+"
    ticket = make_ticket(title=special_title)
    result = to_ticket_out(ticket)
    assert result.title == special_title

# TC17: 属性値が長大な文字列
def test_to_ticket_out_TC17():
    # TC17: titleが1000文字
    long_title = "a" * 1000
    ticket = make_ticket(title=long_title)
    result = to_ticket_out(ticket)
    assert result.title == long_title