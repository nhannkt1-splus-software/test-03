import pytest

# --- テスト用ダミークラス定義 ---
# TicketStatusのダミー定義
class TicketStatus:
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    REOPENED = "REOPENED"
    CLOSED = "CLOSED"

# Ticketのダミー定義
class Ticket:
    def __init__(self, id, status):
        self.id = id
        self.status = status

# TicketNotFoundのダミー定義
class TicketNotFound(Exception):
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id

# TicketClosedErrorのダミー定義
class TicketClosedError(Exception):
    def __init__(self, ticket_id, msg):
        self.ticket_id = ticket_id
        self.msg = msg

# WorklogServiceのダミー定義（本物のメソッドをそのまま利用）
from types import SimpleNamespace

class WorklogService:
    def __init__(self, store):
        self.store = store

    def _get_writable_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.store.get(ticket_id)
        if ticket is None:
            raise TicketNotFound(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketClosedError(ticket.id, "log time on")
        return ticket

# --- テスト用ストアダミー ---
class DummyStore:
    def __init__(self, tickets):
        self.tickets = tickets

    def get(self, ticket_id):
        return self.tickets.get(ticket_id, None)

# --- テストケース ---
# TC1: ticket_id=1, status=OPEN, 正常系
def test_TC1():
    # TC1: 有効なticket_idで、チケットがOPENの場合
    tickets = {1: Ticket(1, TicketStatus.OPEN)}
    service = WorklogService(DummyStore(tickets))
    # チケットが返ることを確認
    result = service._get_writable_ticket(1)
    assert isinstance(result, Ticket)
    assert result.status == TicketStatus.OPEN

# TC2: ticket_id=1, status=IN_PROGRESS, 正常系
def test_TC2():
    # TC2: 有効なticket_idで、チケットがIN_PROGRESSの場合
    tickets = {1: Ticket(1, TicketStatus.IN_PROGRESS)}
    service = WorklogService(DummyStore(tickets))
    result = service._get_writable_ticket(1)
    assert isinstance(result, Ticket)
    assert result.status == TicketStatus.IN_PROGRESS

# TC3: ticket_id=1, status=REOPENED, 正常系
def test_TC3():
    # TC3: 有効なticket_idで、チケットがREOPENEDの場合
    tickets = {1: Ticket(1, TicketStatus.REOPENED)}
    service = WorklogService(DummyStore(tickets))
    result = service._get_writable_ticket(1)
    assert isinstance(result, Ticket)
    assert result.status == TicketStatus.REOPENED

# TC4: ticket_id=1, status=CLOSED, TicketClosedError
def test_TC4():
    # TC4: 有効なticket_idだが、チケットがCLOSEDの場合
    tickets = {1: Ticket(1, TicketStatus.CLOSED)}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketClosedError) as e:
        service._get_writable_ticket(1)
    assert e.value.ticket_id == 1

# TC5: ticket_id=1, チケットが存在しない, TicketNotFound
def test_TC5():
    # TC5: 有効なticket_idだが、チケットが存在しない場合
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketNotFound) as e:
        service._get_writable_ticket(1)
    assert e.value.ticket_id == 1

# TC6: ticket_id=0, status=OPEN, 正常系
def test_TC6():
    # TC6: ticket_idが0（境界値）で、チケットがOPENの場合
    tickets = {0: Ticket(0, TicketStatus.OPEN)}
    service = WorklogService(DummyStore(tickets))
    result = service._get_writable_ticket(0)
    assert isinstance(result, Ticket)
    assert result.status == TicketStatus.OPEN

# TC7: ticket_id=-1, status=OPEN, 正常系
def test_TC7():
    # TC7: ticket_idが負の値で、チケットがOPENの場合
    tickets = {-1: Ticket(-1, TicketStatus.OPEN)}
    service = WorklogService(DummyStore(tickets))
    result = service._get_writable_ticket(-1)
    assert isinstance(result, Ticket)
    assert result.status == TicketStatus.OPEN

# TC8: ticket_id=999999, status=OPEN, 正常系
def test_TC8():
    # TC8: ticket_idが非常に大きい値で、チケットがOPENの場合
    tickets = {999999: Ticket(999999, TicketStatus.OPEN)}
    service = WorklogService(DummyStore(tickets))
    result = service._get_writable_ticket(999999)
    assert isinstance(result, Ticket)
    assert result.status == TicketStatus.OPEN

# TC9: ticket_id=None, TypeError
def test_TC9():
    # TC9: ticket_idがNoneの場合（型不一致）
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TypeError):
        service._get_writable_ticket(None)

# TC10: ticket_id="abc", TypeError
def test_TC10():
    # TC10: ticket_idがstr型の場合（型不一致）
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TypeError):
        service._get_writable_ticket("abc")

# TC11: ticket_id=1.5, TypeError
def test_TC11():
    # TC11: ticket_idがfloat型の場合（型不一致）
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TypeError):
        service._get_writable_ticket(1.5)

# TC12: ticket_id=[], TypeError
def test_TC12():
    # TC12: ticket_idがlist型の場合（型不一致）
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TypeError):
        service._get_writable_ticket([])

# TC13: ticket_id={}, TypeError
def test_TC13():
    # TC13: ticket_idがdict型の場合（型不一致）
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TypeError):
        service._get_writable_ticket({})

# TC14: ticket_id=0, status=CLOSED, TicketClosedError
def test_TC14():
    # TC14: ticket_idが0（境界値）で、チケットがCLOSEDの場合
    tickets = {0: Ticket(0, TicketStatus.CLOSED)}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketClosedError) as e:
        service._get_writable_ticket(0)
    assert e.value.ticket_id == 0

# TC15: ticket_id=0, チケットが存在しない, TicketNotFound
def test_TC15():
    # TC15: ticket_idが0（境界値）で、チケットが存在しない場合
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketNotFound) as e:
        service._get_writable_ticket(0)
    assert e.value.ticket_id == 0

# TC16: ticket_id=-1, status=CLOSED, TicketClosedError
def test_TC16():
    # TC16: ticket_idが負の値で、チケットがCLOSEDの場合
    tickets = {-1: Ticket(-1, TicketStatus.CLOSED)}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketClosedError) as e:
        service._get_writable_ticket(-1)
    assert e.value.ticket_id == -1

# TC17: ticket_id=-1, チケットが存在しない, TicketNotFound
def test_TC17():
    # TC17: ticket_idが負の値で、チケットが存在しない場合
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketNotFound) as e:
        service._get_writable_ticket(-1)
    assert e.value.ticket_id == -1

# TC18: ticket_id=999999, status=CLOSED, TicketClosedError
def test_TC18():
    # TC18: ticket_idが非常に大きい値で、チケットがCLOSEDの場合
    tickets = {999999: Ticket(999999, TicketStatus.CLOSED)}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketClosedError) as e:
        service._get_writable_ticket(999999)
    assert e.value.ticket_id == 999999

# TC19: ticket_id=999999, チケットが存在しない, TicketNotFound
def test_TC19():
    # TC19: ticket_idが非常に大きい値で、チケットが存在しない場合
    tickets = {}
    service = WorklogService(DummyStore(tickets))
    with pytest.raises(TicketNotFound) as e:
        service._get_writable_ticket(999999)
    assert e.value.ticket_id == 999999