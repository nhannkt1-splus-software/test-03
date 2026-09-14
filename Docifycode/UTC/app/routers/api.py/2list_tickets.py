import pytest
from unittest.mock import MagicMock, patch

# --- テスト用のダミークラス・Enum定義 ---
import types

# Priority, TicketStatus, TicketOut, TicketService, to_ticket_out, get_ticket_service をダミー定義
class Priority:
    HIGH = 'HIGH'
    LOW = 'LOW'

class TicketStatus:
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

class TicketOut:
    def __init__(self, id, title):
        self.id = id
        self.title = title

class DummyTicket:
    def __init__(self, id, title):
        self.id = id
        self.title = title

class TicketService:
    def list_tickets(self, status_filter, priority, project_id, q, overdue):
        return []

def to_ticket_out(ticket):
    return TicketOut(ticket.id, ticket.title)

def get_ticket_service():
    return TicketService()

# --- テスト対象関数のimport ---
# テスト対象関数をimport
from fastapi import Query, Depends
import sys

# テスト対象関数を直接importできない場合は、globals()から取得
if 'list_tickets' not in globals():
    # テスト対象モジュール名を'module_under_test'と仮定
    # from module_under_test import list_tickets
    pass

# --- pytest用テスト関数 ---

# TC1: 全てのフィルタが未指定の正常系
def test_TC1_all_filters_none(monkeypatch):
    # テストID: TC1
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(1, "ticket1")]
    monkeypatch.setattr(__name__, "get_ticket_service", lambda: service)
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    from fastapi import Query
    # status_filter, priority, project_id, q, overdue = None
    result = list_tickets(
        status_filter=None,
        priority=None,
        project_id=None,
        q=None,
        overdue=None,
        service=service
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], TicketOut)
    assert result[0].id == 1

# TC2: 全てのフィルタが有効値の正常系
def test_TC2_all_filters_valid(monkeypatch):
    # テストID: TC2
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(2, "bug ticket")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.OPEN,
        priority=Priority.HIGH,
        project_id=1,
        q='bug',
        overdue=True,
        service=service
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == 2
    assert result[0].title == "bug ticket"
    service.list_tickets.assert_called_once_with(TicketStatus.OPEN, Priority.HIGH, 1, 'bug', True)

# TC3: フィルタ指定で該当チケットなしの正常系
def test_TC3_no_ticket_found(monkeypatch):
    # テストID: TC3
    service = MagicMock()
    service.list_tickets.return_value = []
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.CLOSED,
        priority=Priority.LOW,
        project_id=0,
        q='',
        overdue=False,
        service=service
    )
    assert result == []

# TC4: status_filterが無効値の異常系
def test_TC4_invalid_status_filter(monkeypatch):
    # テストID: TC4
    service = MagicMock()
    with pytest.raises(ValueError):
        list_tickets(
            status_filter='INVALID_STATUS',
            priority=None,
            project_id=None,
            q=None,
            overdue=None,
            service=service
        )

# TC5: priorityが無効値の異常系
def test_TC5_invalid_priority(monkeypatch):
    # テストID: TC5
    service = MagicMock()
    with pytest.raises(ValueError):
        list_tickets(
            status_filter=TicketStatus.OPEN,
            priority='INVALID_PRIORITY',
            project_id=None,
            q=None,
            overdue=None,
            service=service
        )

# TC6: project_idが負数の異常系
def test_TC6_negative_project_id(monkeypatch):
    # テストID: TC6
    service = MagicMock()
    with pytest.raises(ValueError):
        list_tickets(
            status_filter=TicketStatus.OPEN,
            priority=Priority.HIGH,
            project_id=-1,
            q=None,
            overdue=None,
            service=service
        )

# TC7: project_idが型違いの異常系
def test_TC7_project_id_type_error(monkeypatch):
    # テストID: TC7
    service = MagicMock()
    with pytest.raises(TypeError):
        list_tickets(
            status_filter=TicketStatus.OPEN,
            priority=Priority.HIGH,
            project_id='abc',
            q=None,
            overdue=None,
            service=service
        )

# TC8: qが長い文字列の正常系
def test_TC8_long_q(monkeypatch):
    # テストID: TC8
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(3, "long q ticket")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    long_q = 'a' * 100
    result = list_tickets(
        status_filter=TicketStatus.OPEN,
        priority=Priority.HIGH,
        project_id=1,
        q=long_q,
        overdue=None,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "long q ticket"

# TC9: overdueが型違いの異常系
def test_TC9_overdue_type_error(monkeypatch):
    # テストID: TC9
    service = MagicMock()
    with pytest.raises(TypeError):
        list_tickets(
            status_filter=TicketStatus.OPEN,
            priority=Priority.HIGH,
            project_id=1,
            q='bug',
            overdue='yes',
            service=service
        )

# TC10: serviceがnullの異常系
def test_TC10_service_is_none():
    # テストID: TC10
    with pytest.raises(TypeError):
        list_tickets(
            status_filter=TicketStatus.OPEN,
            priority=Priority.HIGH,
            project_id=1,
            q='bug',
            overdue=True,
            service=None
        )

# TC11: 正常系で複数件返却
def test_TC11_multiple_tickets(monkeypatch):
    # テストID: TC11
    service = MagicMock()
    service.list_tickets.return_value = [
        DummyTicket(1, "ticket1"),
        DummyTicket(2, "ticket2"),
    ]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.OPEN,
        priority=Priority.HIGH,
        project_id=1,
        q='bug',
        overdue=True,
        service=service
    )
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

# TC12: service.list_ticketsが空リスト返却の正常系
def test_TC12_service_returns_empty(monkeypatch):
    # テストID: TC12
    service = MagicMock()
    service.list_tickets.return_value = []
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.OPEN,
        priority=Priority.HIGH,
        project_id=1,
        q='bug',
        overdue=True,
        service=service
    )
    assert result == []

# TC13: to_ticket_outで型不一致の異常系
def test_TC13_to_ticket_out_type_error(monkeypatch):
    # テストID: TC13
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(1, "ticket1")]
    def bad_to_ticket_out(ticket):
        raise TypeError("型不一致")
    monkeypatch.setattr(__name__, "to_ticket_out", bad_to_ticket_out)
    with pytest.raises(TypeError):
        list_tickets(
            status_filter=TicketStatus.OPEN,
            priority=Priority.HIGH,
            project_id=1,
            q='bug',
            overdue=True,
            service=service
        )

# TC14: q未指定の正常系
def test_TC14_q_none(monkeypatch):
    # テストID: TC14
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(4, "no q ticket")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.OPEN,
        priority=Priority.HIGH,
        project_id=1,
        q=None,
        overdue=None,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "no q ticket"

# TC15: overdueのみ指定の正常系
def test_TC15_overdue_only(monkeypatch):
    # テストID: TC15
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(5, "overdue only")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=None,
        priority=None,
        project_id=None,
        q=None,
        overdue=True,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "overdue only"

# TC16: overdue=falseのみ指定の正常系
def test_TC16_overdue_false_only(monkeypatch):
    # テストID: TC16
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(6, "overdue false only")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=None,
        priority=None,
        project_id=None,
        q=None,
        overdue=False,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "overdue false only"

# TC17: qが空文字列の正常系
def test_TC17_q_empty_string(monkeypatch):
    # テストID: TC17
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(7, "q empty")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.OPEN,
        priority=Priority.LOW,
        project_id=1,
        q='',
        overdue=None,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "q empty"

# TC18: status_filterのみ指定の正常系
def test_TC18_status_filter_only(monkeypatch):
    # テストID: TC18
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(8, "status only")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=TicketStatus.CLOSED,
        priority=None,
        project_id=None,
        q=None,
        overdue=None,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "status only"

# TC19: priorityのみ指定の正常系
def test_TC19_priority_only(monkeypatch):
    # テストID: TC19
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(9, "priority only")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=None,
        priority=Priority.HIGH,
        project_id=None,
        q=None,
        overdue=None,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "priority only"

# TC20: project_idが0の正常系
def test_TC20_project_id_zero(monkeypatch):
    # テストID: TC20
    service = MagicMock()
    service.list_tickets.return_value = [DummyTicket(10, "project id zero")]
    monkeypatch.setattr(__name__, "to_ticket_out", to_ticket_out)
    result = list_tickets(
        status_filter=None,
        priority=None,
        project_id=0,
        q=None,
        overdue=None,
        service=service
    )
    assert len(result) == 1
    assert result[0].title == "project id zero"