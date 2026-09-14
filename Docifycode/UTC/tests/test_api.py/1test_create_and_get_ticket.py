import pytest
from fastapi.testclient import TestClient

# テスト対象APIのFastAPIアプリをimport
# from app import app

# テスト用のクライアント生成
# client = TestClient(app)

# 認証情報の有無や権限を切り替えるためのヘルパー関数
def get_client(auth: str = "valid"):
    """
    認証情報や権限を切り替えたTestClientを返す
    auth: "valid", "none", "invalid", "forbidden"
    """
    # 実際の実装では、TestClientのヘッダやミドルウェアを切り替える
    # ここでは例としてheadersを切り替える
    from app import app  # テスト対象のFastAPIアプリ
    client = TestClient(app)
    if auth == "valid":
        client.headers.update({"Authorization": "Bearer validtoken"})
    elif auth == "invalid":
        client.headers.update({"Authorization": "Bearer invalidtoken"})
    elif auth == "forbidden":
        client.headers.update({"Authorization": "Bearer forbiddentoken"})
    # "none"の場合はAuthorizationヘッダなし
    return client

# -------------------------------
# TC1: 正常系：title, priorityともに正常値（high）
def test_TC1_create_and_get_ticket_high():
    # TC1
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 201
    ticket_id = res.json()["id"]
    fetched = client.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 200
    data = fetched.json()
    assert data["title"] == "API ticket"
    assert data["priority"] == "high"
    assert data["id"] == ticket_id

# TC2: 正常系：priorityがlow
def test_TC2_create_and_get_ticket_low():
    # TC2
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "low"})
    assert res.status_code == 201
    ticket_id = res.json()["id"]
    fetched = client.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 200
    data = fetched.json()
    assert data["title"] == "API ticket"
    assert data["priority"] == "low"
    assert data["id"] == ticket_id

# TC3: 正常系：priorityがmedium
def test_TC3_create_and_get_ticket_medium():
    # TC3
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "medium"})
    assert res.status_code == 201
    ticket_id = res.json()["id"]
    fetched = client.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 200
    data = fetched.json()
    assert data["title"] == "API ticket"
    assert data["priority"] == "medium"
    assert data["id"] == ticket_id

# TC4: 異常系：titleが空文字
def test_TC4_create_ticket_title_empty():
    # TC4
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "", "priority": "high"})
    assert res.status_code == 400

# TC5: 異常系：priorityが空文字
def test_TC5_create_ticket_priority_empty():
    # TC5
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": ""})
    assert res.status_code == 400

# TC6: 異常系：priorityが欠落
def test_TC6_create_ticket_priority_missing():
    # TC6
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket"})
    assert res.status_code == 400

# TC7: 異常系：titleが欠落
def test_TC7_create_ticket_title_missing():
    # TC7
    client = get_client("valid")
    res = client.post("/api/tickets", json={"priority": "high"})
    assert res.status_code == 400

# TC8: 異常系：titleがint型
def test_TC8_create_ticket_title_int():
    # TC8
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": 123, "priority": "high"})
    assert res.status_code == 400

# TC9: 異常系：priorityがint型
def test_TC9_create_ticket_priority_int():
    # TC9
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": 1})
    assert res.status_code == 400

# TC10: 異常系：titleとpriority両方欠落
def test_TC10_create_ticket_both_missing():
    # TC10
    client = get_client("valid")
    res = client.post("/api/tickets", json={})
    assert res.status_code == 400

# TC11: 異常系：jsonがnull
def test_TC11_create_ticket_json_null():
    # TC11
    client = get_client("valid")
    res = client.post("/api/tickets", json=None)
    assert res.status_code == 400

# TC12: 異常系：priorityが不正値
def test_TC12_create_ticket_priority_invalid():
    # TC12
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "invalid_priority"})
    assert res.status_code == 400

# TC13: 異常系：認証情報なし（POST）
def test_TC13_create_ticket_no_auth():
    # TC13
    client = get_client("none")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 401

# TC14: 異常系：無効な認証情報（POST）
def test_TC14_create_ticket_invalid_auth():
    # TC14
    client = get_client("invalid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 401

# TC15: 異常系：GET時に認証情報なし
def test_TC15_get_ticket_no_auth():
    # TC15
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 201
    ticket_id = res.json()["id"]
    client_no_auth = get_client("none")
    fetched = client_no_auth.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 401

# TC16: 異常系：GET時に無効な認証情報
def test_TC16_get_ticket_invalid_auth():
    # TC16
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 201
    ticket_id = res.json()["id"]
    client_invalid = get_client("invalid")
    fetched = client_invalid.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 401

# TC17: 異常系：GET時に権限不足
def test_TC17_get_ticket_forbidden():
    # TC17
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 201
    ticket_id = res.json()["id"]
    client_forbidden = get_client("forbidden")
    fetched = client_forbidden.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 403

# TC18: 異常系：POST時に権限不足
def test_TC18_create_ticket_forbidden():
    # TC18
    client = get_client("forbidden")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 403

# TC19: 異常系：GETで存在しないticket_idを指定
def test_TC19_get_ticket_not_found():
    # TC19
    client = get_client("valid")
    # 存在しないIDを指定（例: 99999）
    fetched = client.get("/api/tickets/99999")
    assert fetched.status_code == 404

# TC20: 異常系：重複などの競合（POST）
def test_TC20_create_ticket_conflict():
    # TC20
    client = get_client("valid")
    # 1回目は正常
    res1 = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res1.status_code == 201
    # 2回目、同じ内容で競合を発生させる
    res2 = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res2.status_code == 409

# TC21: 異常系：created.json()やfetched.json()で'id'や'title'が存在しない場合
def test_TC21_create_ticket_missing_fields_in_response():
    # TC21
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    assert res.status_code == 201
    # 'id'が存在しない場合をシミュレート
    data = res.json()
    assert "id" in data
    ticket_id = data["id"]
    fetched = client.get(f"/api/tickets/{ticket_id}")
    fetched_data = fetched.json()
    assert "title" in fetched_data
    assert "priority" in fetched_data
    assert "id" in fetched_data

# TC22: 異常系：client.postやclient.getの引数型不一致時
def test_TC22_create_ticket_invalid_argument_type():
    # TC22
    client = get_client("valid")
    # json引数にstr型を渡す（本来はdict型）
    with pytest.raises(Exception):
        client.post("/api/tickets", json="not a dict")
    # getのパスにint型を渡す（本来はstr型）
    with pytest.raises(Exception):
        client.get(12345)

# TC23: 異常系：status_codeやレスポンス内容が期待値と異なる場合
def test_TC23_create_ticket_unexpected_status_or_response():
    # TC23
    client = get_client("valid")
    res = client.post("/api/tickets", json={"title": "API ticket", "priority": "high"})
    # 期待値は201
    assert res.status_code == 201, f"期待した201だが、実際は{res.status_code}"
    data = res.json()
    assert data.get("title") == "API ticket", f"titleが期待値と異なる: {data.get('title')}"
    assert data.get("priority") == "high", f"priorityが期待値と異なる: {data.get('priority')}"
    assert "id" in data, "idがレスポンスに含まれていない"
    ticket_id = data["id"]
    fetched = client.get(f"/api/tickets/{ticket_id}")
    assert fetched.status_code == 200, f"期待した200だが、実際は{fetched.status_code}"
    fetched_data = fetched.json()
    assert fetched_data.get("title") == "API ticket", f"GETのtitleが期待値と異なる: {fetched_data.get('title')}"
    assert fetched_data.get("priority") == "high", f"GETのpriorityが期待値と異なる: {fetched_data.get('priority')}"
    assert fetched_data.get("id") == ticket_id, f"GETのidが期待値と異なる: {fetched_data.get('id')}"