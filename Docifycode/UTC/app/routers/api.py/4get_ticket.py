import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError

# --- テスト対象のrouterを含むFastAPIアプリをインポート ---
# router, TicketService, TicketNotFound, http_error, to_ticket_out, get_ticket_service, TicketOut
# これらはテスト対象モジュールからインポートしてください
# 例: from app_module import router, TicketService, TicketNotFound, http_error, to_ticket_out, get_ticket_service, TicketOut

# テスト用のFastAPIアプリを作成し、routerを登録
app = FastAPI()
app.include_router(router)

# テストクライアントを作成
client = TestClient(app)

# --- TicketServiceのモックを作成 ---
class MockTicketService:
    def get_ticket(self, ticket_id):
        # TC1: ticket_id=1 の場合、正常なチケット情報を返す
        if ticket_id == 1:
            # ダミーのチケット情報を返す
            return {"id": 1, "title": "Test Ticket", "description": "Test Description"}
        # TC2, TC3, TC4: ticket_idが存在しない場合、TicketNotFound例外を発生させる
        elif ticket_id in [999999, 0, -1]:
            raise TicketNotFound(f"Ticket {ticket_id} not found")
        # その他は通常の動作
        else:
            raise TicketNotFound(f"Ticket {ticket_id} not found")

# --- get_ticket_serviceの依存性をモックに差し替える ---
app.dependency_overrides[get_ticket_service] = lambda: MockTicketService()

# --- テストケース ---

# TC1: ticket_id=1（正常系）
def test_get_ticket_tc1():
    # テストID: TC1
    # ticket_id=1 を指定し、正常なチケット情報が返ることを確認
    response = client.get("/tickets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Ticket"
    assert data["description"] == "Test Description"

# TC2: ticket_id=999999（存在しないID）
def test_get_ticket_tc2():
    # テストID: TC2
    # ticket_id=999999 を指定し、TicketNotFound例外がhttp_errorで変換されることを確認
    response = client.get("/tickets/999999")
    assert response.status_code == 404  # http_errorが404を返す想定
    # エラーメッセージの内容を確認（必要に応じて）
    assert "not found" in response.text.lower()

# TC3: ticket_id=0（境界値）
def test_get_ticket_tc3():
    # テストID: TC3
    # ticket_id=0 を指定し、TicketNotFound例外がhttp_errorで変換されることを確認
    response = client.get("/tickets/0")
    assert response.status_code == 404  # http_errorが404を返す想定
    assert "not found" in response.text.lower()

# TC4: ticket_id=-1（負の値）
def test_get_ticket_tc4():
    # テストID: TC4
    # ticket_id=-1 を指定し、TicketNotFound例外がhttp_errorで変換されることを確認
    response = client.get("/tickets/-1")
    assert response.status_code == 404  # http_errorが404を返す想定
    assert "not found" in response.text.lower()

# TC5: ticket_id="abc"（型不一致: str型）
def test_get_ticket_tc5():
    # テストID: TC5
    # ticket_id="abc" を指定し、バリデーションエラーが発生することを確認
    response = client.get("/tickets/abc")
    assert response.status_code == 422  # FastAPIのバリデーションエラー
    # バリデーションエラーの内容を確認
    assert "value is not a valid integer" in response.text.lower()

# TC6: ticket_id=None（Noneが渡された場合）
def test_get_ticket_tc6():
    # テストID: TC6
    # ticket_id=None を指定し、バリデーションエラーが発生することを確認
    # NoneはURLパスパラメータとして渡せないため、空文字列でテスト
    response = client.get("/tickets/")
    assert response.status_code == 404  # パスが不正な場合は404になる
    # ただし、FastAPIの仕様上、パスパラメータが欠落すると404になる

# TC7: ticket_id=1.5（型不一致: float型）
def test_get_ticket_tc7():
    # テストID: TC7
    # ticket_id=1.5 を指定し、バリデーションエラーが発生することを確認
    response = client.get("/tickets/1.5")
    assert response.status_code == 422  # FastAPIのバリデーションエラー
    assert "value is not a valid integer" in response.text.lower()