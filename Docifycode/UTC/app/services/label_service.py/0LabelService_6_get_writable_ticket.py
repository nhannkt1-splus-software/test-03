import pytest

# テスト用のダミークラスと例外を定義
class TicketStatus:
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"

class Ticket:
    def __init__(self, id, status):
        self.id = id
        self.status = status

class TicketNotFound(Exception):
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id

class TicketClosedError(Exception):
    def __init__(self, ticket_id, context):
        self.ticket_id = ticket_id
        self.context = context

# LabelServiceのテスト用ダミーstoreを作成
class DummyStore:
    def __init__(self, tickets):
        self.tickets = tickets

    def get(self, ticket_id):
        return self.tickets.get(ticket_id, None)

# LabelServiceインスタンスを作成するヘルパー
def make_label_service(store):
    svc = LabelService()
    svc.store = store
    return svc

# --- テストケース ---

# TC1: ticketが存在し、statusがOPENの場合
def test_get_writable_ticket_TC1():
    # チケット準備
    ticket_id = 1
    ticket = Ticket(ticket_id, TicketStatus.OPEN)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    # 実行・検証
    assert svc._get_writable_ticket(ticket_id) == ticket  # 正常系

# TC2: ticketが存在し、statusがIN_PROGRESSの場合
def test_get_writable_ticket_TC2():
    ticket_id = 1
    ticket = Ticket(ticket_id, TicketStatus.IN_PROGRESS)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    assert svc._get_writable_ticket(ticket_id) == ticket  # 正常系

# TC3: ticketが存在し、statusがCLOSEDの場合
def test_get_writable_ticket_TC3():
    ticket_id = 1
    ticket = Ticket(ticket_id, TicketStatus.CLOSED)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    with pytest.raises(TicketClosedError):  # 異常系
        svc._get_writable_ticket(ticket_id)

# TC4: ticketが存在しない場合
def test_get_writable_ticket_TC4():
    ticket_id = 1
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TicketNotFound):  # 異常系
        svc._get_writable_ticket(ticket_id)

# TC5: ticket_idが0で、ticketが存在し、statusがOPENの場合
def test_get_writable_ticket_TC5():
    ticket_id = 0
    ticket = Ticket(ticket_id, TicketStatus.OPEN)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    assert svc._get_writable_ticket(ticket_id) == ticket  # 境界値

# TC6: ticket_idが負の値で、ticketが存在し、statusがOPENの場合
def test_get_writable_ticket_TC6():
    ticket_id = -1
    ticket = Ticket(ticket_id, TicketStatus.OPEN)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    assert svc._get_writable_ticket(ticket_id) == ticket  # 境界値

# TC7: ticket_idが非常に大きい値で、ticketが存在し、statusがOPENの場合
def test_get_writable_ticket_TC7():
    ticket_id = 999999
    ticket = Ticket(ticket_id, TicketStatus.OPEN)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    assert svc._get_writable_ticket(ticket_id) == ticket  # 境界値

# TC8: ticket_idがstr型の場合（型不一致）
def test_get_writable_ticket_TC8():
    ticket_id = "1"
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TypeError):  # 型不一致
        svc._get_writable_ticket(ticket_id)

# TC9: ticket_idがNone型の場合（型不一致）
def test_get_writable_ticket_TC9():
    ticket_id = None
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TypeError):  # 型不一致
        svc._get_writable_ticket(ticket_id)

# TC10: ticket_idがfloat型の場合（型不一致）
def test_get_writable_ticket_TC10():
    ticket_id = 1.5
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TypeError):  # 型不一致
        svc._get_writable_ticket(ticket_id)

# TC11: ticket_idが0で、ticketが存在しない場合
def test_get_writable_ticket_TC11():
    ticket_id = 0
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TicketNotFound):  # 境界値
        svc._get_writable_ticket(ticket_id)

# TC12: ticket_idが負の値で、ticketが存在しない場合
def test_get_writable_ticket_TC12():
    ticket_id = -1
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TicketNotFound):  # 境界値
        svc._get_writable_ticket(ticket_id)

# TC13: ticket_idが非常に大きい値で、ticketが存在しない場合
def test_get_writable_ticket_TC13():
    ticket_id = 999999
    store = DummyStore({})
    svc = make_label_service(store)
    with pytest.raises(TicketNotFound):  # 境界値
        svc._get_writable_ticket(ticket_id)

# TC14: ticket_idが0で、ticketが存在し、statusがCLOSEDの場合
def test_get_writable_ticket_TC14():
    ticket_id = 0
    ticket = Ticket(ticket_id, TicketStatus.CLOSED)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    with pytest.raises(TicketClosedError):  # 境界値
        svc._get_writable_ticket(ticket_id)

# TC15: ticket_idが負の値で、ticketが存在し、statusがCLOSEDの場合
def test_get_writable_ticket_TC15():
    ticket_id = -1
    ticket = Ticket(ticket_id, TicketStatus.CLOSED)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    with pytest.raises(TicketClosedError):  # 境界値
        svc._get_writable_ticket(ticket_id)

# TC16: ticket_idが非常に大きい値で、ticketが存在し、statusがCLOSEDの場合
def test_get_writable_ticket_TC16():
    ticket_id = 999999
    ticket = Ticket(ticket_id, TicketStatus.CLOSED)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    with pytest.raises(TicketClosedError):  # 境界値
        svc._get_writable_ticket(ticket_id)

# TC17: ticket_idが1で、ticketが存在し、statusがOPENの場合（重複確認）
def test_get_writable_ticket_TC17():
    ticket_id = 1
    ticket = Ticket(ticket_id, TicketStatus.OPEN)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    assert svc._get_writable_ticket(ticket_id) == ticket  # 正常系（重複）

# TC18: ticket_idが1で、ticketが存在し、statusがIN_PROGRESSの場合（重複確認）
def test_get_writable_ticket_TC18():
    ticket_id = 1
    ticket = Ticket(ticket_id, TicketStatus.IN_PROGRESS)
    store = DummyStore({ticket_id: ticket})
    svc = make_label_service(store)
    assert svc._get_writable_ticket(ticket_id) == ticket  # 正常系（重複）
```
