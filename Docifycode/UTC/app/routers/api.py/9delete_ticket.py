import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# テスト対象のFastAPIアプリと依存関数をimport
from your_module import app, get_ticket_service, DeskError

client = TestClient(app)

# --- TC1: 正常系：ticket_idが存在し、削除が成功するケース ---
# ticket_id=1, 期待される結果: None（例外なし、204 No Content）
def test_delete_ticket_tc1():
    # テストID: TC1
    mock_service = MagicMock()
    mock_service.delete_ticket.return_value = None
    # 依存性注入をモックに差し替え
    app.dependency_overrides[get_ticket_service] = lambda: mock_service

    response = client.delete("/tickets/1")
    # 204 No Contentが返ることを確認
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # レスポンスボディは空
    assert response.content == b""

    # 依存性のオーバーライドを解除
    app.dependency_overrides = {}

# --- TC2: ticket_idが存在しない場合、DeskErrorが発生するケース ---
# ticket_id=999999, 期待される結果: DeskError
def test_delete_ticket_tc2():
    # テストID: TC2
    def raise_desk_error(ticket_id):
        raise DeskError("not found")
    mock_service = MagicMock()
    mock_service.delete_ticket.side_effect = raise_desk_error
    app.dependency_overrides[get_ticket_service] = lambda: mock_service

    response = client.delete("/tickets/999999")
    # FastAPIの例外ハンドラによるエラー応答（例: 400, 404, 422など）を想定
    # DeskError→http_error→HTTPExceptionに変換される前提
    assert response.status_code >= 400
    # エラーメッセージに"not found"が含まれることを確認
    assert b"not found" in response.content

    app.dependency_overrides = {}

# --- TC3: ticket_idが境界値（0）の場合、DeskErrorが発生するケース ---
# ticket_id=0, 期待される結果: DeskError
def test_delete_ticket_tc3():
    # テストID: TC3
    def raise_desk_error(ticket_id):
        raise DeskError("not found")
    mock_service = MagicMock()
    mock_service.delete_ticket.side_effect = raise_desk_error
    app.dependency_overrides[get_ticket_service] = lambda: mock_service

    response = client.delete("/tickets/0")
    assert response.status_code >= 400
    assert b"not found" in response.content

    app.dependency_overrides = {}

# --- TC4: ticket_idが負の値の場合、DeskErrorが発生するケース ---
# ticket_id=-1, 期待される結果: DeskError
def test_delete_ticket_tc4():
    # テストID: TC4
    def raise_desk_error(ticket_id):
        raise DeskError("not found")
    mock_service = MagicMock()
    mock_service.delete_ticket.side_effect = raise_desk_error
    app.dependency_overrides[get_ticket_service] = lambda: mock_service

    response = client.delete("/tickets/-1")
    assert response.status_code >= 400
    assert b"not found" in response.content

    app.dependency_overrides = {}

# --- TC5: ticket_idがstr型の場合、TypeErrorが発生するケース ---
# ticket_id="abc", 期待される結果: TypeError
def test_delete_ticket_tc5():
    # テストID: TC5
    # FastAPIのパスパラメータがint型なので、"abc"は422 Unprocessable Entityになる
    response = client.delete("/tickets/abc")
    # 422エラーが返ることを確認
    assert response.status_code == 422
    # エラーメッセージに"type"や"int"が含まれることを確認
    assert b"type" in response.content or b"int" in response.content

# --- TC6: ticket_idがNoneの場合、TypeErrorが発生するケース ---
# ticket_id=None, 期待される結果: TypeError
def test_delete_ticket_tc6():
    # テストID: TC6
    # NoneはURLで表現できないため、パスパラメータが欠落した場合をテスト
    response = client.delete("/tickets/")
    # 404 Not Foundが返ることを確認
    assert response.status_code == 404
    # エラーメッセージに"path"や"not found"が含まれることを確認
    assert b"path" in response.content or b"not found" in response.content