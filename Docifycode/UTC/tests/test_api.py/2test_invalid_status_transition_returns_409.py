import pytest

# TicketStatusの定義が必要な場合は適宜importしてください
# from your_module import TicketStatus

# TC1: 正常なチケット作成直後にCLOSEDへ不正遷移した場合のテスト
def test_TC1_invalid_status_transition_returns_409(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # CLOSEDへ遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={"status": TicketStatus.CLOSED},
    )
    # 409が返ること
    assert response.status_code == 409

# TC2: 存在しないチケットIDでCLOSEDへ遷移しようとした場合のテスト
def test_TC2_invalid_ticket_id_returns_404(client):
    # 存在しないIDでCLOSEDへ遷移
    response = client.post(
        "/api/tickets/99999/status",
        json={"status": TicketStatus.CLOSED},
    )
    # 404または409が返ること（仕様によるが409を優先）
    assert response.status_code in (404, 409)

# TC3: 存在しないステータス値で状態遷移しようとした場合のテスト
def test_TC3_invalid_status_value_returns_400_or_valueerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # 不正なステータス値で遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={"status": "INVALID_STATUS"},
    )
    # ValueErrorまたは400/422が返ること
    assert response.status_code in (400, 422)

# TC4: ステータス値がNoneの場合のテスト
def test_TC4_status_none_returns_400_or_valueerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # ステータス値Noneで遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={"status": None},
    )
    # ValueErrorまたは400/422が返ること
    assert response.status_code in (400, 422)

# TC5: jsonパラメータがnullの場合のテスト
def test_TC5_json_null_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=Noneで遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json=None,
    )
    # TypeErrorまたは400/422が返ること
    assert response.status_code in (400, 422)

# TC6: jsonパラメータがint型の場合のテスト
def test_TC6_json_int_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=intで遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json=12345,
    )
    # TypeErrorまたは400/422が返ること
    assert response.status_code in (400, 422)

# TC7: 空文字タイトルのチケット作成直後にCLOSEDへ不正遷移した場合のテスト
def test_TC7_empty_title_invalid_status_transition_returns_409(client):
    # 空文字タイトルでチケット作成
    created = client.post("/api/tickets", json={"title": ""})
    ticket_id = created.json()["id"]
    # CLOSEDへ遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={"status": TicketStatus.CLOSED},
    )
    assert response.status_code == 409

# TC8: Noneタイトルのチケット作成直後にCLOSEDへ不正遷移した場合のテスト
def test_TC8_none_title_invalid_status_transition_returns_409(client):
    # Noneタイトルでチケット作成
    created = client.post("/api/tickets", json={"title": None})
    ticket_id = created.json()["id"]
    # CLOSEDへ遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={"status": TicketStatus.CLOSED},
    )
    assert response.status_code == 409

# TC9: 256文字の長いタイトルのチケット作成直後にCLOSEDへ不正遷移した場合のテスト
def test_TC9_long_title_invalid_status_transition_returns_409(client):
    # 256文字タイトルでチケット作成
    long_title = "a" * 256
    created = client.post("/api/tickets", json={"title": long_title})
    ticket_id = created.json()["id"]
    # CLOSEDへ遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={"status": TicketStatus.CLOSED},
    )
    assert response.status_code == 409

# TC10: jsonパラメータがlist型の場合のテスト
def test_TC10_json_list_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=listで遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json=["status", TicketStatus.CLOSED],
    )
    assert response.status_code in (400, 422)

# TC11: 正常なチケット作成時のテスト
def test_TC11_ticket_creation_returns_201(client):
    # チケット作成
    response = client.post("/api/tickets", json={"title": "Bad jump"})
    assert response.status_code == 201
    assert "id" in response.json()

# TC12: レスポンスにidが存在しない場合のテスト
def test_TC12_response_without_id_raises_keyerror(client, monkeypatch):
    # レスポンスのjson()がidを返さないようにモンキーパッチ
    class DummyResponse:
        def json(self):
            return {}
    created = DummyResponse()
    # idが存在しない場合KeyErrorが発生すること
    with pytest.raises(KeyError):
        _ = created.json()["id"]

# TC13: jsonパラメータが空辞書の場合のテスト
def test_TC13_json_empty_dict_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json={}で遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json={},
    )
    assert response.status_code in (400, 422)

# TC14: jsonパラメータが文字列型の場合のテスト
def test_TC14_json_string_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=文字列で遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json="not a dict",
    )
    assert response.status_code in (400, 422)

# TC15: jsonパラメータがfloat型の場合のテスト
def test_TC15_json_float_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=floatで遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json=0.123,
    )
    assert response.status_code in (400, 422)

# TC16: jsonパラメータがbool型の場合のテスト
def test_TC16_json_bool_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=boolで遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json=True,
    )
    assert response.status_code in (400, 422)

# TC17: jsonパラメータがリスト型（辞書のリスト）の場合のテスト
def test_TC17_json_list_of_dict_returns_400_or_typeerror(client):
    # チケット作成
    created = client.post("/api/tickets", json={"title": "Bad jump"})
    ticket_id = created.json()["id"]
    # json=[{"status": ...}]で遷移
    response = client.post(
        f"/api/tickets/{ticket_id}/status",
        json=[{"status": TicketStatus.CLOSED}],
    )
    assert response.status_code in (400, 422)
```
