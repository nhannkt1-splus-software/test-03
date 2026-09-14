import pytest
from uuid import UUID

# テスト対象のクラスや例外、Enumをインポート
# ここでは仮定として、TicketService, TicketStatus, InvalidStatusTransition, NotFoundExceptionが
# test対象モジュールからインポートできるものとする
from target_module import TicketService, TicketStatus, InvalidStatusTransition, NotFoundException

# TC1: 正常なインスタンスでチケット作成後CLOSEDに変更しようとする場合（不正な遷移）
def test_TC1_change_status_invalid_transition():
    # TC1
    service = TicketService()
    ticket = service.create_ticket(title="Skip path")
    with pytest.raises(InvalidStatusTransition):
        service.change_status(ticket.id, TicketStatus.CLOSED)

# TC2: チケットが既にCLOSED状態の場合にCLOSEDへ変更しようとするケース
def test_TC2_change_status_already_closed():
    # TC2
    service = TicketService()
    ticket = service.create_ticket(title="Already closed")
    service.change_status(ticket.id, TicketStatus.CLOSED)
    with pytest.raises(InvalidStatusTransition):
        service.change_status(ticket.id, TicketStatus.CLOSED)

# TC3: ticket.idが存在しない場合
def test_TC3_change_status_not_found():
    # TC3
    service = TicketService()
    invalid_id = 99999999  # 存在しないID
    with pytest.raises(NotFoundException):
        service.change_status(invalid_id, TicketStatus.CLOSED)

# TC4: ticket.idがNoneの場合
def test_TC4_change_status_id_none():
    # TC4
    service = TicketService()
    with pytest.raises(TypeError):
        service.change_status(None, TicketStatus.CLOSED)

# TC5: ticket.idがstr型など不正な型の場合
def test_TC5_change_status_id_str():
    # TC5
    service = TicketService()
    with pytest.raises(TypeError):
        service.change_status("abc", TicketStatus.CLOSED)

# TC6: statusがTicketStatus型以外の場合（str型）
def test_TC6_change_status_status_str():
    # TC6
    service = TicketService()
    ticket = service.create_ticket(title="Invalid status type")
    with pytest.raises(TypeError):
        service.change_status(ticket.id, "CLOSED")

# TC7: serviceがNoneの場合
def test_TC7_change_status_service_none():
    # TC7
    service = None
    ticket_id = 1  # 仮の有効なID
    with pytest.raises(TypeError):
        # serviceがNoneなので、インスタンスメソッド呼び出しでTypeErrorが発生する
        service.change_status(ticket_id, TicketStatus.CLOSED)

# TC8: serviceがint型など不正な型の場合
def test_TC8_change_status_service_int():
    # TC8
    service = 123
    ticket_id = 1  # 仮の有効なID
    with pytest.raises(TypeError):
        # int型にはchange_statusメソッドがないためTypeErrorが発生する
        service.change_status(ticket_id, TicketStatus.CLOSED)

# TC9: serviceが内部的に異常状態の場合
def test_TC9_change_status_service_abnormal_state():
    # TC9
    service = TicketService()
    # 内部状態を異常にする（例えば、チケット管理辞書を空にするなど）
    # ここでは仮定として、_tickets属性が存在するとする
    service._tickets = None
    ticket = service.create_ticket(title="Abnormal state")
    with pytest.raises(InvalidStatusTransition):
        service.change_status(ticket.id, TicketStatus.CLOSED)

# TC10: ticket.idがfloat型など不正な型の場合
def test_TC10_change_status_id_float():
    # TC10
    service = TicketService()
    with pytest.raises(TypeError):
        service.change_status(1.5, TicketStatus.CLOSED)

# TC11: statusがint型などTicketStatus型以外の場合
def test_TC11_change_status_status_int():
    # TC11
    service = TicketService()
    ticket = service.create_ticket(title="Invalid status int")
    with pytest.raises(TypeError):
        service.change_status(ticket.id, 123)

# TC12: statusがNone型の場合
def test_TC12_change_status_status_none():
    # TC12
    service = TicketService()
    ticket = service.create_ticket(title="Invalid status None")
    with pytest.raises(TypeError):
        service.change_status(ticket.id, None)

# TC13: serviceがstr型など不正な型の場合
def test_TC13_change_status_service_str():
    # TC13
    service = "service"
    ticket_id = 1  # 仮の有効なID
    with pytest.raises(TypeError):
        # str型にはchange_statusメソッドがないためTypeErrorが発生する
        service.change_status(ticket_id, TicketStatus.CLOSED)

# TC14: ticket.idがUUID型で有効な場合（正常な遷移で不正な状態遷移）
def test_TC14_change_status_id_uuid():
    # TC14
    service = TicketService()
    uuid_id = UUID('123e4567-e89b-12d3-a456-426614174000')
    # UUID型でチケットを作成できる場合を仮定
    ticket = service.create_ticket(title="UUID id", id=uuid_id)
    with pytest.raises(InvalidStatusTransition):
        service.change_status(uuid_id, TicketStatus.CLOSED)
```
