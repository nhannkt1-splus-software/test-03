import pytest
from datetime import datetime
from types import SimpleNamespace

# --- テスト用ダミー定義 ---
# TicketStatusのダミーEnum
class TicketStatus:
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    INVALID = "INVALID"

# Ticketのダミークラス
class Ticket:
    def __init__(self, ticket_id, status):
        self.id = ticket_id
        self.status = status
        self.updated_at = None

# 例外クラス
class InvalidStatusTransition(Exception):
    def __init__(self, current, target):
        self.current = current
        self.target = target

class NotFoundError(Exception):
    pass

# ALLOWED_TRANSITIONSのダミー定義
ALLOWED_TRANSITIONS = {
    TicketStatus.OPEN: [TicketStatus.PENDING, TicketStatus.CLOSED],
    TicketStatus.PENDING: [TicketStatus.RESOLVED, TicketStatus.CLOSED],
    TicketStatus.RESOLVED: [TicketStatus.CLOSED],
    TicketStatus.CLOSED: [],
}

# utc_nowのダミー
def utc_now():
    return datetime(2024, 6, 1, 12, 0, 0)

# --- テスト対象クラスのダミー実装 ---
from target_module import TicketService  # 実際のテストでは対象モジュールをimport

# --- テスト用ヘルパー ---
class DummyTicketService(TicketService):
    def __init__(self):
        super().__init__()
        # チケットDBのダミー
        self.tickets = {
            1: Ticket(1, TicketStatus.OPEN),
            100: Ticket(100, "UNKNOWN_STATUS"),
        }
        # 状態ごとのテスト用チケット
        self.status_tickets = {
            TicketStatus.OPEN: Ticket(1, TicketStatus.OPEN),
            TicketStatus.PENDING: Ticket(1, TicketStatus.PENDING),
            TicketStatus.CLOSED: Ticket(1, TicketStatus.CLOSED),
            TicketStatus.RESOLVED: Ticket(1, TicketStatus.RESOLVED),
        }

    def get_ticket(self, ticket_id):
        # ticket_idがNoneや型不正の場合
        if ticket_id is None or not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        # ticket_idが0以下の場合
        if ticket_id <= 0:
            raise NotFoundError("ticket not found")
        # 存在しないticket_id
        if ticket_id not in self.tickets:
            raise NotFoundError("ticket not found")
        return self.tickets[ticket_id]

    # テスト用：ticket_idとstatusを指定してチケットをセット
    def set_ticket_status(self, ticket_id, status):
        self.tickets[ticket_id] = Ticket(ticket_id, status)

# --- テストケース ---
@pytest.fixture
def service():
    return DummyTicketService()

# TC1: targetが現在のstatusと同じ場合
def test_TC1_same_status(service):
    # チケットのstatusをOPENにセット
    service.set_ticket_status(1, TicketStatus.OPEN)
    # targetもOPEN
    ticket = service.change_status(1, TicketStatus.OPEN)
    # 変更されていないことを確認
    assert ticket.status == TicketStatus.OPEN
    assert ticket.updated_at is None  # 更新されていない
    # TC1

# TC2: 許可されたstatus遷移（OPEN→CLOSED）
def test_TC2_allowed_transition_open_to_closed(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    ticket = service.change_status(1, TicketStatus.CLOSED)
    assert ticket.status == TicketStatus.CLOSED
    assert ticket.updated_at == utc_now()
    # TC2

# TC3: 許可されていないstatus遷移（OPEN→INVALID）
def test_TC3_invalid_transition_open_to_invalid(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    with pytest.raises(InvalidStatusTransition):
        service.change_status(1, TicketStatus.INVALID)
    # TC3

# TC4: 存在しないticket_id
def test_TC4_not_found_ticket_id(service):
    with pytest.raises(NotFoundError):
        service.change_status(9999, TicketStatus.OPEN)
    # TC4

# TC5: ticket_idが負の値
def test_TC5_negative_ticket_id(service):
    with pytest.raises(NotFoundError):
        service.change_status(-1, TicketStatus.OPEN)
    # TC5

# TC6: ticket_idがNone
def test_TC6_ticket_id_none(service):
    with pytest.raises(TypeError):
        service.change_status(None, TicketStatus.OPEN)
    # TC6

# TC7: ticket_idが文字列
def test_TC7_ticket_id_string(service):
    with pytest.raises(TypeError):
        service.change_status("abc", TicketStatus.OPEN)
    # TC7

# TC8: ticket_idが0
def test_TC8_ticket_id_zero(service):
    with pytest.raises(NotFoundError):
        service.change_status(0, TicketStatus.OPEN)
    # TC8

# TC9: ALLOWED_TRANSITIONSに存在しないstatusのチケット
def test_TC9_ticket_status_not_in_allowed_transitions(service):
    # statusがALLOWED_TRANSITIONSに存在しない
    service.set_ticket_status(100, "UNKNOWN_STATUS")
    with pytest.raises(KeyError):
        service.change_status(100, TicketStatus.OPEN)
    # TC9

# TC10: targetがNone
def test_TC10_target_none(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    with pytest.raises(TypeError):
        service.change_status(1, None)
    # TC10

# TC11: targetが文字列
def test_TC11_target_string(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    with pytest.raises(TypeError):
        service.change_status(1, "string")
    # TC11

# TC12: targetがint型
def test_TC12_target_int(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    with pytest.raises(TypeError):
        service.change_status(1, 123)
    # TC12

# TC13: targetがリスト型
def test_TC13_target_list(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    with pytest.raises(TypeError):
        service.change_status(1, [])
    # TC13

# TC14: OPEN→PENDINGへの許可されたstatus遷移
def test_TC14_allowed_transition_open_to_pending(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    ticket = service.change_status(1, TicketStatus.PENDING)
    assert ticket.status == TicketStatus.PENDING
    assert ticket.updated_at == utc_now()
    # TC14

# TC15: OPEN→RESOLVEDへの許可されていないstatus遷移
def test_TC15_invalid_transition_open_to_resolved(service):
    service.set_ticket_status(1, TicketStatus.OPEN)
    with pytest.raises(InvalidStatusTransition):
        service.change_status(1, TicketStatus.RESOLVED)
    # TC15

# TC16: PENDING→CLOSEDへの許可されたstatus遷移
def test_TC16_allowed_transition_pending_to_closed(service):
    service.set_ticket_status(1, TicketStatus.PENDING)
    ticket = service.change_status(1, TicketStatus.CLOSED)
    assert ticket.status == TicketStatus.CLOSED
    assert ticket.updated_at == utc_now()
    # TC16

# TC17: CLOSED→OPENへの許可されていないstatus遷移
def test_TC17_invalid_transition_closed_to_open(service):
    service.set_ticket_status(1, TicketStatus.CLOSED)
    with pytest.raises(InvalidStatusTransition):
        service.change_status(1, TicketStatus.OPEN)
    # TC17

# TC18: RESOLVED→CLOSEDへの許可されたstatus遷移
def test_TC18_allowed_transition_resolved_to_closed(service):
    service.set_ticket_status(1, TicketStatus.RESOLVED)
    ticket = service.change_status(1, TicketStatus.CLOSED)
    assert ticket.status == TicketStatus.CLOSED
    assert ticket.updated_at == utc_now()
    # TC18

# TC19: PENDING→RESOLVEDへの許可されたstatus遷移
def test_TC19_allowed_transition_pending_to_resolved(service):
    service.set_ticket_status(1, TicketStatus.PENDING)
    ticket = service.change_status(1, TicketStatus.RESOLVED)
    assert ticket.status == TicketStatus.RESOLVED
    assert ticket.updated_at == utc_now()
    # TC19

# TC20: CLOSED→PENDINGへの許可されていないstatus遷移
def test_TC20_invalid_transition_closed_to_pending(service):
    service.set_ticket_status(1, TicketStatus.CLOSED)
    with pytest.raises(InvalidStatusTransition):
        service.change_status(1, TicketStatus.PENDING)
    # TC20