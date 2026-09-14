import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, Depends
from pydantic import ValidationError

# --- テスト対象関数の依存クラス・関数のダミー定義 ---
# 本来はimportするが、テストのために最低限のダミーを用意
class DeskError(Exception):
    pass

class TicketOut:
    def __init__(self, id, status):
        self.id = id
        self.status = status

class TicketStatusChange:
    def __init__(self, status):
        # statusは"open"または"closed"のみ許容
        if status not in ("open", "closed"):
            raise ValidationError([{"loc": ("status",), "msg": "invalid status", "type": "value_error"}], TicketStatusChange)
        self.status = status

def to_ticket_out(ticket):
    # ticketはdictまたはTicketOut想定
    if isinstance(ticket, dict):
        return TicketOut(**ticket)
    return ticket

def http_error(exc):
    # DeskErrorをHTTPExceptionに変換
    return HTTPException(status_code=400, detail=str(exc))

# --- テスト対象関数のimport ---
# change_statusはrouter.postのデコレータがついているが、関数自体は直接importできる前提
from types import SimpleNamespace

# テスト対象関数の再定義（実際はimportする）
def change_status(
    ticket_id: int,
    payload: TicketStatusChange,
    service,
) -> TicketOut:
    try:
        return to_ticket_out(service.change_status(ticket_id, payload.status))
    except DeskError as exc:
        raise http_error(exc) from exc

# --- テストケース ---
# 各テストケースで使うモックサービス
class MockTicketService:
    def __init__(self, should_raise=False, ticket=None):
        self.should_raise = should_raise
        self.ticket = ticket or {"id": 1, "status": "open"}
    def change_status(self, ticket_id, status):
        if self.should_raise:
            raise DeskError("error")
        return {"id": ticket_id, "status": status}

# --- テスト本体 ---

# TC1: 正常系：ticket_idとpayloadが正常、status=open
def test_change_status_tc1():
    # TC1
    service = MockTicketService()
    payload = TicketStatusChange("open")
    result = change_status(1, payload, service)
    assert isinstance(result, TicketOut)
    assert result.id == 1
    assert result.status == "open"

# TC2: 正常系：ticket_idとpayloadが正常、status=closed
def test_change_status_tc2():
    # TC2
    service = MockTicketService()
    payload = TicketStatusChange("closed")
    result = change_status(1, payload, service)
    assert isinstance(result, TicketOut)
    assert result.id == 1
    assert result.status == "closed"

# TC3: 境界値テスト：ticket_id=0
def test_change_status_tc3():
    # TC3
    service = MockTicketService()
    payload = TicketStatusChange("open")
    result = change_status(0, payload, service)
    assert isinstance(result, TicketOut)
    assert result.id == 0
    assert result.status == "open"

# TC4: 異常系：ticket_idが負の値
def test_change_status_tc4():
    # TC4
    service = MockTicketService()
    payload = TicketStatusChange("open")
    result = change_status(-1, payload, service)
    assert isinstance(result, TicketOut)
    assert result.id == -1
    assert result.status == "open"

# TC5: 境界値テスト：非常に大きいticket_id
def test_change_status_tc5():
    # TC5
    service = MockTicketService()
    payload = TicketStatusChange("open")
    big_id = 999999999
    result = change_status(big_id, payload, service)
    assert isinstance(result, TicketOut)
    assert result.id == big_id
    assert result.status == "open"

# TC6: 異常系：ticket_idがstr型（型不一致）
def test_change_status_tc6():
    # TC6
    service = MockTicketService()
    payload = TicketStatusChange("open")
    with pytest.raises(TypeError):
        change_status("1", payload, service)

# TC7: 異常系：ticket_idがNone（型不一致）
def test_change_status_tc7():
    # TC7
    service = MockTicketService()
    payload = TicketStatusChange("open")
    with pytest.raises(TypeError):
        change_status(None, payload, service)

# TC8: 異常系：payload.statusが不正な値
def test_change_status_tc8():
    # TC8
    service = MockTicketService()
    with pytest.raises(ValidationError):
        TicketStatusChange("invalid_status")

# TC9: 異常系：payloadが空のdict（型不一致）
def test_change_status_tc9():
    # TC9
    service = MockTicketService()
    # dictを直接渡すとTypeError
    with pytest.raises(TypeError):
        change_status(1, {}, service)

# TC10: 異常系：payloadがNone（型不一致）
def test_change_status_tc10():
    # TC10
    service = MockTicketService()
    with pytest.raises(AttributeError):
        # None.statusでAttributeError
        change_status(1, None, service)

# TC11: 異常系：service.change_statusでDeskError発生
def test_change_status_tc11():
    # TC11
    service = MockTicketService(should_raise=True)
    payload = TicketStatusChange("open")
    with pytest.raises(HTTPException) as excinfo:
        change_status(1, payload, service)
    assert excinfo.value.status_code == 400

# TC12: 異常系：status=closedでservice.change_statusがDeskErrorを発生
def test_change_status_tc12():
    # TC12
    service = MockTicketService(should_raise=True)
    payload = TicketStatusChange("closed")
    with pytest.raises(HTTPException) as excinfo:
        change_status(1, payload, service)
    assert excinfo.value.status_code == 400

# TC13: 異常系：ticket_id=0, status=closedでservice.change_statusがDeskErrorを発生
def test_change_status_tc13():
    # TC13
    service = MockTicketService(should_raise=True)
    payload = TicketStatusChange("closed")
    with pytest.raises(HTTPException) as excinfo:
        change_status(0, payload, service)
    assert excinfo.value.status_code == 400

# TC14: 異常系：ticket_idが負の値、status=closedでservice.change_statusがDeskErrorを発生
def test_change_status_tc14():
    # TC14
    service = MockTicketService(should_raise=True)
    payload = TicketStatusChange("closed")
    with pytest.raises(HTTPException) as excinfo:
        change_status(-1, payload, service)
    assert excinfo.value.status_code == 400

# TC15: 異常系：非常に大きいticket_id、status=closedでservice.change_statusがDeskErrorを発生
def test_change_status_tc15():
    # TC15
    service = MockTicketService(should_raise=True)
    payload = TicketStatusChange("closed")
    big_id = 999999999
    with pytest.raises(HTTPException) as excinfo:
        change_status(big_id, payload, service)
    assert excinfo.value.status_code == 400