import pytest

# --- テスト用ダミークラス定義 ---
# TicketStatusのダミーEnum
class TicketStatus:
    OPEN = 'open'
    CLOSED = 'closed'

# チケットのダミークラス
class Ticket:
    def __init__(self, status):
        self.status = status

# TicketServiceのダミークラス
class TicketService:
    def __init__(self, tickets):
        self._tickets = tickets

    def list_tickets(self, status=None):
        # statusが不正な型の場合TypeError
        if status is not None and not isinstance(status, str):
            raise TypeError("status must be str or None")
        # statusがstr型だがOPEN/CLOSED以外の場合TypeError
        if status is not None and status not in (TicketStatus.OPEN, TicketStatus.CLOSED):
            raise TypeError("invalid status value")
        # チケットデータが不正な場合TypeError
        for ticket in self._tickets:
            if ticket is not None and not hasattr(ticket, 'status'):
                raise TypeError("invalid ticket data")
        if status is None:
            return self._tickets
        return [ticket for ticket in self._tickets if ticket is not None and ticket.status == status]

# --- テスト対象関数 ---
from types import SimpleNamespace

def test_list_tickets_can_filter_by_status(service):
    open_tickets = service.list_tickets(status=TicketStatus.OPEN)
    assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
    assert len(open_tickets) == 1

# --- テストケース ---
# TC1: OPENチケットが1件のみ存在する場合（正常系）
def test_TC1():
    # TC1
    # OPENチケット1件のみ
    service = TicketService([Ticket(TicketStatus.OPEN)])
    test_list_tickets_can_filter_by_status(service)

# TC2: OPENチケットが複数件存在する場合（異常系）
def test_TC2():
    # TC2
    # OPENチケット2件
    service = TicketService([Ticket(TicketStatus.OPEN), Ticket(TicketStatus.OPEN)])
    with pytest.raises(AssertionError):
        test_list_tickets_can_filter_by_status(service)

# TC3: OPENチケットが0件（異常系）
def test_TC3():
    # TC3
    # OPENチケットなし
    service = TicketService([Ticket(TicketStatus.CLOSED)])
    with pytest.raises(AssertionError):
        test_list_tickets_can_filter_by_status(service)

# TC4: status未指定（None）（異常系）
def test_TC4():
    # TC4
    # OPEN/CLOSED混在
    service = TicketService([Ticket(TicketStatus.OPEN), Ticket(TicketStatus.CLOSED)])
    # test_list_tickets_can_filter_by_statusはstatus=OPENで呼ぶが、内部でstatus=Noneを渡すにはラップ
    def wrapper(service):
        open_tickets = service.list_tickets(status=None)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(AssertionError):
        wrapper(service)

# TC5: serviceがNone（異常系）
def test_TC5():
    # TC5
    service = None
    with pytest.raises(AttributeError):
        test_list_tickets_can_filter_by_status(service)

# TC6: serviceがstr型（異常系）
def test_TC6():
    # TC6
    service = "invalid_type"
    with pytest.raises(AttributeError):
        test_list_tickets_can_filter_by_status(service)

# TC7: statusがstr型の不正値（異常系）
def test_TC7():
    # TC7
    service = TicketService([Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status='invalid_status')
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC8: statusがint型の不正値（異常系）
def test_TC8():
    # TC8
    service = TicketService([Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=999)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC9: チケットデータが不正（異常系）
def test_TC9():
    # TC9
    service = TicketService([None, SimpleNamespace(status=TicketStatus.OPEN), "invalid_ticket"])
    with pytest.raises(TypeError):
        test_list_tickets_can_filter_by_status(service)

# TC10: OPENチケット1件のみ保持しているがstatus未指定（異常系）
def test_TC10():
    # TC10
    service = TicketService([Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=None)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(AssertionError):
        wrapper(service)

# TC11: OPENチケット0件でstatus未指定（異常系）
def test_TC11():
    # TC11
    service = TicketService([Ticket(TicketStatus.CLOSED)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=None)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(AssertionError):
        wrapper(service)

# TC12: OPENチケット複数件保持しているがstatus未指定（異常系）
def test_TC12():
    # TC12
    service = TicketService([Ticket(TicketStatus.OPEN), Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=None)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(AssertionError):
        wrapper(service)

# TC13: OPENチケット1件のみ保持しているがstatusがstr型の不正値（異常系）
def test_TC13():
    # TC13
    service = TicketService([Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status='invalid_status')
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC14: OPENチケット1件のみ保持しているがstatusがint型の不正値（異常系）
def test_TC14():
    # TC14
    service = TicketService([Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=999)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC15: OPENチケット複数件保持しているがstatusがstr型の不正値（異常系）
def test_TC15():
    # TC15
    service = TicketService([Ticket(TicketStatus.OPEN), Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status='invalid_status')
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC16: OPENチケット複数件保持しているがstatusがint型の不正値（異常系）
def test_TC16():
    # TC16
    service = TicketService([Ticket(TicketStatus.OPEN), Ticket(TicketStatus.OPEN)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=999)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC17: OPENチケット0件保持しているがstatusがstr型の不正値（異常系）
def test_TC17():
    # TC17
    service = TicketService([Ticket(TicketStatus.CLOSED)])
    def wrapper(service):
        open_tickets = service.list_tickets(status='invalid_status')
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)

# TC18: OPENチケット0件保持しているがstatusがint型の不正値（異常系）
def test_TC18():
    # TC18
    service = TicketService([Ticket(TicketStatus.CLOSED)])
    def wrapper(service):
        open_tickets = service.list_tickets(status=999)
        assert all(ticket.status == TicketStatus.OPEN for ticket in open_tickets)
        assert len(open_tickets) == 1
    with pytest.raises(TypeError):
        wrapper(service)