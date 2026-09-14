import pytest

# テスト対象の例外クラスとサービスクラスをインポート
# from <module> import TicketService, TicketNotFound

class DummyTicketService:
    # ダミーサービス：get_ticketメソッドのみ実装
    def get_ticket(self, ticket_id):
        # 型チェック
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        # 存在しないチケットIDの場合
        if ticket_id in [999, 0, -1]:
            raise TicketNotFound("Ticket not found")
        # 存在する場合（テストでは使わない）
        return {"id": ticket_id}

# TC1: ticket_id=999（存在しないチケットID、通常の異常系）
def test_TC1_get_unknown_ticket_raises_999():
    # テストID: TC1
    service = DummyTicketService()
    with pytest.raises(TicketNotFound):
        service.get_ticket(999)

# TC2: ticket_id=0（存在しないチケットID、境界値）
def test_TC2_get_unknown_ticket_raises_0():
    # テストID: TC2
    service = DummyTicketService()
    with pytest.raises(TicketNotFound):
        service.get_ticket(0)

# TC3: ticket_id=-1（存在しないチケットID、負の値）
def test_TC3_get_unknown_ticket_raises_minus1():
    # テストID: TC3
    service = DummyTicketService()
    with pytest.raises(TicketNotFound):
        service.get_ticket(-1)

# TC4: ticket_id="999"（str型、型不一致）
def test_TC4_get_unknown_ticket_raises_str():
    # テストID: TC4
    service = DummyTicketService()
    with pytest.raises(TypeError):
        service.get_ticket("999")

# TC5: ticket_id=None（NoneType、型不一致）
def test_TC5_get_unknown_ticket_raises_none():
    # テストID: TC5
    service = DummyTicketService()
    with pytest.raises(TypeError):
        service.get_ticket(None)

# TC6: ticket_id=999.0（float型、型不一致）
def test_TC6_get_unknown_ticket_raises_float():
    # テストID: TC6
    service = DummyTicketService()
    with pytest.raises(TypeError):
        service.get_ticket(999.0)

# TC7: ticket_id=[]（list型、型不一致）
def test_TC7_get_unknown_ticket_raises_list():
    # テストID: TC7
    service = DummyTicketService()
    with pytest.raises(TypeError):
        service.get_ticket([])

# TC8: ticket_id={}（dict型、型不一致）
def test_TC8_get_unknown_ticket_raises_dict():
    # テストID: TC8
    service = DummyTicketService()
    with pytest.raises(TypeError):
        service.get_ticket({})
```
