import pytest

# テスト用のダミークラス定義（本番コードの型定義に合わせる）
class Ticket:
    pass

class TicketNotFound(Exception):
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        super().__init__(f"Ticket not found: {ticket_id}")

# テスト対象クラスのインスタンス生成用ヘルパー
def create_ticket_service(store_dict):
    svc = TicketService()
    # store属性をテスト用にセット
    svc.store = store_dict
    return svc

# TC1: ticket_id=1（正常系：有効なticket_id）
def test_get_ticket_tc1():
    # テストID: TC1
    svc = create_ticket_service({1: Ticket()})
    ticket = svc.get_ticket(1)
    # Ticketインスタンスが返ることを確認
    assert isinstance(ticket, Ticket)

# TC2: ticket_id=999（異常系：存在しないticket_id）
def test_get_ticket_tc2():
    # テストID: TC2
    svc = create_ticket_service({1: Ticket()})
    with pytest.raises(TicketNotFound) as excinfo:
        svc.get_ticket(999)
    # ticket_idが例外に含まれていることを確認
    assert excinfo.value.ticket_id == 999

# TC3: ticket_id=0（境界値テスト）
def test_get_ticket_tc3():
    # テストID: TC3
    # 0が有効なIDの場合
    svc_valid = create_ticket_service({0: Ticket()})
    ticket = svc_valid.get_ticket(0)
    assert isinstance(ticket, Ticket)
    # 0が無効なIDの場合
    svc_invalid = create_ticket_service({})
    with pytest.raises(TicketNotFound) as excinfo:
        svc_invalid.get_ticket(0)
    assert excinfo.value.ticket_id == 0

# TC4: ticket_id=-1（異常系：負のticket_id）
def test_get_ticket_tc4():
    # テストID: TC4
    svc = create_ticket_service({1: Ticket()})
    with pytest.raises(TicketNotFound) as excinfo:
        svc.get_ticket(-1)
    assert excinfo.value.ticket_id == -1

# TC5: ticket_id="1"（異常系：str型）
def test_get_ticket_tc5():
    # テストID: TC5
    svc = create_ticket_service({1: Ticket()})
    with pytest.raises(TypeError):
        svc.get_ticket("1")

# TC6: ticket_id=None（異常系：None型）
def test_get_ticket_tc6():
    # テストID: TC6
    svc = create_ticket_service({1: Ticket()})
    with pytest.raises(TypeError):
        svc.get_ticket(None)

# TC7: ticket_id=1.5（異常系：float型）
def test_get_ticket_tc7():
    # テストID: TC7
    svc = create_ticket_service({1: Ticket()})
    with pytest.raises(TypeError):
        svc.get_ticket(1.5)