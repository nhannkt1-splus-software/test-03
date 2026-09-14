import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from pydantic import ValidationError
from unittest.mock import MagicMock, patch

# --- 必要なクラス・例外・関数のダミー定義 ---
# 本来はimportするが、テストのためにダミーを用意
class DeskError(Exception):
    pass

class Ticket:
    def __init__(self, ticket_id, username):
        self.ticket_id = ticket_id
        self.username = username

class TicketOut:
    def __init__(self, ticket_id, username):
        self.ticket_id = ticket_id
        self.username = username

class TicketAssign:
    def __init__(self, username):
        if username is None:
            raise ValidationError("username is required", TicketAssign)
        self.username = username

class TicketService:
    def assign(self, ticket_id, username):
        pass

def to_ticket_out(ticket):
    return TicketOut(ticket.ticket_id, ticket.username)

def http_error(exc):
    raise exc

# FastAPIアプリとルータのダミー
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

# 実際のassign_ticket関数をimportする場合はここでimport
# from yourmodule import assign_ticket

# テスト対象関数をrouterに追加
@router.post("/tickets/{ticket_id}/assign", response_model=TicketOut)
def assign_ticket(
    ticket_id: int,
    payload: TicketAssign,
    service: TicketService = Depends(lambda: TicketService()),
) -> TicketOut:
    try:
        return to_ticket_out(service.assign(ticket_id, payload.username))
    except DeskError as exc:
        raise http_error(exc) from exc

app.include_router(router)

client = TestClient(app)

# --- テストケース ---

# TC1: 正常系：有効なticket_idと有効なusernameの場合
def test_TC1_assign_ticket_valid(monkeypatch):
    # service.assignのモック
    def mock_assign(self, ticket_id, username):
        return Ticket(ticket_id, username)
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/1/assign", json=payload)
    # 期待値: 200 OK, 正常なレスポンス
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == 1
    assert data["username"] == "valid_user"

# TC2: 異常系：usernameが存在しない場合
def test_TC2_assign_ticket_nonexistent_user(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("User does not exist")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "nonexistent_user"}
    response = client.post("/tickets/1/assign", json=payload)
    # 期待値: 500 Internal Server Error (DeskError)
    assert response.status_code == 500

# TC3: 異常系：ticket_idが0の場合
def test_TC3_assign_ticket_ticket_id_zero(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("Invalid ticket_id")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/0/assign", json=payload)
    assert response.status_code == 500

# TC4: 異常系：ticket_idが負の場合
def test_TC4_assign_ticket_ticket_id_negative(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("Negative ticket_id")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/-1/assign", json=payload)
    assert response.status_code == 500

# TC5: 異常系：usernameが空文字の場合
def test_TC5_assign_ticket_username_empty(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("Empty username")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": ""}
    response = client.post("/tickets/1/assign", json=payload)
    assert response.status_code == 500

# TC6: 境界値テスト：非常に大きいticket_id。存在しない場合はDeskError、存在する場合は正常
@pytest.mark.parametrize("exists,expected_status", [
    (True, 200),   # 存在する場合
    (False, 500),  # 存在しない場合
])
def test_TC6_assign_ticket_ticket_id_large(monkeypatch, exists, expected_status):
    def mock_assign(self, ticket_id, username):
        if exists:
            return Ticket(ticket_id, username)
        else:
            raise DeskError("ticket_id does not exist")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/999999999/assign", json=payload)
    assert response.status_code == expected_status

# TC7: 異常系：ticket_idが文字列型（型不一致）
def test_TC7_assign_ticket_ticket_id_str():
    payload = {"username": "valid_user"}
    response = client.post("/tickets/abc/assign", json=payload)
    # FastAPIは422 Unprocessable Entityを返す
    assert response.status_code == 422

# TC8: 異常系：payloadがnull（型不一致）
def test_TC8_assign_ticket_payload_null():
    response = client.post("/tickets/1/assign", json=None)
    # FastAPIは422 Unprocessable Entityを返す
    assert response.status_code == 422

# TC9: 異常系：payloadにusernameが未指定
def test_TC9_assign_ticket_payload_empty_dict():
    response = client.post("/tickets/1/assign", json={})
    # FastAPIは422 Unprocessable Entityを返す
    assert response.status_code == 422

# TC10: 異常系：ticket_idがnull（型不一致）
def test_TC10_assign_ticket_ticket_id_null():
    payload = {"username": "valid_user"}
    # URLにnullは指定できないので、空文字で送信
    response = client.post("/tickets//assign", json=payload)
    # FastAPIは404 Not Foundを返す
    assert response.status_code == 404

# TC11: 正常系：service.assignが正常に動作し、TicketOutインスタンスが返されるケース
def test_TC11_assign_ticket_service_assign_returns_ticket(monkeypatch):
    def mock_assign(self, ticket_id, username):
        return Ticket(ticket_id, username)
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/1/assign", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == 1
    assert data["username"] == "valid_user"

# TC12: 異常系：service.assignでユーザーが存在しない場合
def test_TC12_assign_ticket_service_assign_user_not_exist(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("User does not exist")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "nonexistent_user"}
    response = client.post("/tickets/1/assign", json=payload)
    assert response.status_code == 500

# TC13: 異常系：service.assignでticket_idが無効な場合
def test_TC13_assign_ticket_service_assign_ticket_id_zero(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("Invalid ticket_id")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/0/assign", json=payload)
    assert response.status_code == 500

# TC14: 異常系：service.assignでticket_idが負の場合
def test_TC14_assign_ticket_service_assign_ticket_id_negative(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("Negative ticket_id")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/-1/assign", json=payload)
    assert response.status_code == 500

# TC15: 異常系：service.assignでusernameが空の場合
def test_TC15_assign_ticket_service_assign_username_empty(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("Empty username")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": ""}
    response = client.post("/tickets/1/assign", json=payload)
    assert response.status_code == 500

# TC16: 異常系：service.assignでticket_idが存在しない場合
def test_TC16_assign_ticket_service_assign_ticket_id_not_exist(monkeypatch):
    def mock_assign(self, ticket_id, username):
        raise DeskError("ticket_id does not exist")
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/999999999/assign", json=payload)
    assert response.status_code == 500

# TC17: 正常系：service.assignでticket_idが非常に大きいが存在する場合
def test_TC17_assign_ticket_service_assign_ticket_id_large_exists(monkeypatch):
    def mock_assign(self, ticket_id, username):
        return Ticket(ticket_id, username)
    monkeypatch.setattr(TicketService, "assign", mock_assign)
    payload = {"username": "valid_user"}
    response = client.post("/tickets/999999999/assign", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == 999999999
    assert data["username"] == "valid_user"