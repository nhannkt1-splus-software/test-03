import pytest

# --- テスト用ダミークラスと例外定義 ---
# TicketStatusのダミーEnum
class TicketStatus:
    OPEN = 'open'
    PENDING = 'pending'
    RESOLVED = 'resolved'
    CLOSED = 'closed'

# Ticketのダミークラス
class Ticket:
    def __init__(self, id, status):
        self.id = id
        self.status = status

# TicketClosedErrorのダミー例外
class TicketClosedError(Exception):
    def __init__(self, ticket_id, action):
        self.ticket_id = ticket_id
        self.action = action

# --- テスト対象クラスのインポート ---
from target_module import TicketService  # テスト対象モジュール名に合わせて修正してください

# --- テストケース ---
# TC1: チケットがOPEN、actionが'close'の場合、例外は発生しない
def test_TC1():
    # TC1
    ticket = Ticket(1, TicketStatus.OPEN)
    action = 'close'
    # 例外が発生しないことを確認
    TicketService._ensure_not_closed(ticket, action)

# TC2: チケットがPENDING、actionが'update'の場合、例外は発生しない
def test_TC2():
    # TC2
    ticket = Ticket(3, TicketStatus.PENDING)
    action = 'update'
    TicketService._ensure_not_closed(ticket, action)

# TC3: チケットがRESOLVED、actionが'reopen'の場合、例外は発生しない
def test_TC3():
    # TC3
    ticket = Ticket(4, TicketStatus.RESOLVED)
    action = 'reopen'
    TicketService._ensure_not_closed(ticket, action)

# TC4: チケットがCLOSED、actionが'close'の場合、TicketClosedErrorが発生
def test_TC4():
    # TC4
    ticket = Ticket(2, TicketStatus.CLOSED)
    action = 'close'
    with pytest.raises(TicketClosedError) as e:
        TicketService._ensure_not_closed(ticket, action)
    # 例外の内容確認
    assert e.value.ticket_id == 2
    assert e.value.action == 'close'

# TC5: チケットがCLOSED、actionが'update'の場合、TicketClosedErrorが発生
def test_TC5():
    # TC5
    ticket = Ticket(2, TicketStatus.CLOSED)
    action = 'update'
    with pytest.raises(TicketClosedError) as e:
        TicketService._ensure_not_closed(ticket, action)
    assert e.value.ticket_id == 2
    assert e.value.action == 'update'

# TC6: チケットがCLOSED、actionが空文字の場合、TicketClosedErrorが発生
def test_TC6():
    # TC6
    ticket = Ticket(2, TicketStatus.CLOSED)
    action = ''
    with pytest.raises(TicketClosedError) as e:
        TicketService._ensure_not_closed(ticket, action)
    assert e.value.ticket_id == 2
    assert e.value.action == ''

# TC7: チケットがCLOSED、actionがNoneの場合、TicketClosedErrorが発生
def test_TC7():
    # TC7
    ticket = Ticket(2, TicketStatus.CLOSED)
    action = None
    with pytest.raises(TicketClosedError) as e:
        TicketService._ensure_not_closed(ticket, action)
    assert e.value.ticket_id == 2
    assert e.value.action is None

# TC8: ticketがNoneの場合、AttributeErrorが発生
def test_TC8():
    # TC8
    ticket = None
    action = 'close'
    with pytest.raises(AttributeError):
        TicketService._ensure_not_closed(ticket, action)

# TC9: ticketがstr型の場合、AttributeErrorが発生
def test_TC9():
    # TC9
    ticket = 'not_a_ticket'
    action = 'update'
    with pytest.raises(AttributeError):
        TicketService._ensure_not_closed(ticket, action)

# TC10: ticketがint型の場合、AttributeErrorが発生
def test_TC10():
    # TC10
    ticket = 123
    action = 'reopen'
    with pytest.raises(AttributeError):
        TicketService._ensure_not_closed(ticket, action)

# TC11: チケットがOPEN、actionが空文字の場合、例外は発生しない
def test_TC11():
    # TC11
    ticket = Ticket(1, TicketStatus.OPEN)
    action = ''
    TicketService._ensure_not_closed(ticket, action)

# TC12: チケットがOPEN、actionがNoneの場合、例外は発生しない
def test_TC12():
    # TC12
    ticket = Ticket(1, TicketStatus.OPEN)
    action = None
    TicketService._ensure_not_closed(ticket, action)

# TC13: チケットがPENDING、actionが空文字の場合、例外は発生しない
def test_TC13():
    # TC13
    ticket = Ticket(3, TicketStatus.PENDING)
    action = ''
    TicketService._ensure_not_closed(ticket, action)

# TC14: チケットがPENDING、actionがNoneの場合、例外は発生しない
def test_TC14():
    # TC14
    ticket = Ticket(3, TicketStatus.PENDING)
    action = None
    TicketService._ensure_not_closed(ticket, action)

# TC15: チケットがRESOLVED、actionが空文字の場合、例外は発生しない
def test_TC15():
    # TC15
    ticket = Ticket(4, TicketStatus.RESOLVED)
    action = ''
    TicketService._ensure_not_closed(ticket, action)

# TC16: チケットがRESOLVED、actionがNoneの場合、例外は発生しない
def test_TC16():
    # TC16
    ticket = Ticket(4, TicketStatus.RESOLVED)
    action = None
    TicketService._ensure_not_closed(ticket, action)