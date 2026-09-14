import pytest

# テスト用のダミー例外クラス
class NotFoundError(Exception):
    pass

class CustomClosedError(Exception):
    pass

# テスト用のダミーチケットクラス
class DummyTicket:
    def __init__(self, ticket_id, closed=False):
        self.id = ticket_id
        self.closed = closed

# TicketServiceのテスト用サブクラス
class TestableTicketService:
    def __init__(self, get_ticket_behavior=None, ensure_not_closed_behavior=None, store_delete_behavior=None):
        self.get_ticket_behavior = get_ticket_behavior
        self.ensure_not_closed_behavior = ensure_not_closed_behavior
        self.store_delete_behavior = store_delete_behavior
        self.store = self

    # get_ticketのモック
    def get_ticket(self, ticket_id):
        if self.get_ticket_behavior:
            return self.get_ticket_behavior(ticket_id)
        return DummyTicket(ticket_id)

    # _ensure_not_closedのモック
    def _ensure_not_closed(self, ticket, action):
        if self.ensure_not_closed_behavior:
            return self.ensure_not_closed_behavior(ticket, action)
        if getattr(ticket, 'closed', False):
            raise ValueError("Ticket is closed")

    # store.deleteのモック
    def delete(self, ticket_id):
        if self.store_delete_behavior:
            return self.store_delete_behavior(ticket_id)
        # 通常は何もしない

    # delete_ticketの本物の実装をそのまま使う
    def delete_ticket(self, ticket_id: int) -> None:
        ticket = self.get_ticket(ticket_id)
        self._ensure_not_closed(ticket, "delete")
        self.store.delete(ticket_id)

# --- テストケース ---

# TC1: 正常系：存在するチケットIDを削除するケース
def test_delete_ticket_TC1():
    # チケットが存在し、クローズされていない
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: DummyTicket(ticket_id),
        ensure_not_closed_behavior=None,
        store_delete_behavior=None
    )
    # ticket_id=1
    service.delete_ticket(1)  # 例外が発生しないこと

# TC2: 異常系：存在しないチケットIDを指定した場合、get_ticketがNotFoundErrorを投げるケース
def test_delete_ticket_TC2():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: (_ for _ in ()).throw(NotFoundError())
    )
    with pytest.raises(NotFoundError):
        service.delete_ticket(9999)

# TC3: 境界値テスト：0を指定した場合、チケットが存在しないケース
def test_delete_ticket_TC3():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: (_ for _ in ()).throw(NotFoundError())
    )
    with pytest.raises(NotFoundError):
        service.delete_ticket(0)

# TC4: 異常系：負の値を指定した場合、チケットが存在しないケース
def test_delete_ticket_TC4():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: (_ for _ in ()).throw(NotFoundError())
    )
    with pytest.raises(NotFoundError):
        service.delete_ticket(-1)

# TC5: 異常系：ticket_idが文字列型の場合、型不一致によるTypeError
def test_delete_ticket_TC5():
    service = TestableTicketService()
    with pytest.raises(TypeError):
        service.delete_ticket("abc")

# TC6: 異常系：ticket_idがNoneの場合、型不一致によるTypeError
def test_delete_ticket_TC6():
    service = TestableTicketService()
    with pytest.raises(TypeError):
        service.delete_ticket(None)

# TC7: 異常系：ticket_idがfloat型の場合、型不一致によるTypeError
def test_delete_ticket_TC7():
    service = TestableTicketService()
    with pytest.raises(TypeError):
        service.delete_ticket(1.5)

# TC8: 異常系：存在するがクローズ済みのチケットIDを削除しようとした場合
def test_delete_ticket_TC8():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: DummyTicket(ticket_id, closed=True),
        ensure_not_closed_behavior=None
    )
    with pytest.raises(ValueError):
        service.delete_ticket(1)

# TC9: 異常系：クローズ済みチケット削除時にCustomClosedErrorを投げるケース
def test_delete_ticket_TC9():
    def ensure_not_closed(ticket, action):
        raise CustomClosedError()
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: DummyTicket(ticket_id, closed=True),
        ensure_not_closed_behavior=ensure_not_closed
    )
    with pytest.raises(CustomClosedError):
        service.delete_ticket(1)

# TC10: 異常系：store.deleteでKeyErrorを投げるケース（get_ticketが正常にチケットを返すが、store.deleteで例外）
def test_delete_ticket_TC10():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: DummyTicket(ticket_id),
        store_delete_behavior=lambda ticket_id: (_ for _ in ()).throw(KeyError())
    )
    with pytest.raises(KeyError):
        service.delete_ticket(9999)

# TC11: 境界値テスト：int型の最大値を指定した場合、チケットが存在しないケース
def test_delete_ticket_TC11():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: (_ for _ in ()).throw(NotFoundError())
    )
    with pytest.raises(NotFoundError):
        service.delete_ticket(2147483647)

# TC12: 境界値テスト：int型の最小値を指定した場合、チケットが存在しないケース
def test_delete_ticket_TC12():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: (_ for _ in ()).throw(NotFoundError())
    )
    with pytest.raises(NotFoundError):
        service.delete_ticket(-2147483648)

# TC13: 異常系：get_ticketと_ensure_not_closedは正常だが、store.deleteでKeyErrorが発生するケース
def test_delete_ticket_TC13():
    service = TestableTicketService(
        get_ticket_behavior=lambda ticket_id: DummyTicket(ticket_id),
        ensure_not_closed_behavior=None,
        store_delete_behavior=lambda ticket_id: (_ for _ in ()).throw(KeyError())
    )
    with pytest.raises(KeyError):
        service.delete_ticket(1)