import pytest
from fastapi.testclient import TestClient

# テスト対象のFastAPIアプリをインポート
from main import app  # main.pyにFastAPIアプリが定義されていると仮定

client = TestClient(app)

# TC1: 正常系 GETリクエストでヘルスチェックエンドポイントにアクセス
def test_health_get_success():  # TC1
    # TC1: 正しいGETリクエスト
    response = client.get("/health")
    assert response.status_code == 200  # 正常応答
    # レスポンス内容はTC9で詳細に確認

# TC2: 異常系 POSTリクエストでアクセスした場合、許可されていないメソッド
def test_health_post_method_not_allowed():  # TC2
    # TC2: POSTリクエスト
    response = client.post("/health")
    assert response.status_code == 405  # Method Not Allowed

# TC3: 異常系 存在しないエンドポイントにアクセスした場合
def test_healthz_not_found():  # TC3
    # TC3: 存在しないエンドポイント
    response = client.get("/healthz")
    assert response.status_code == 404  # Not Found

# TC4: 正常系 返却値がHealthOut型インスタンスであることを確認
def test_health_response_model_instance():  # TC4
    # TC4: GETリクエスト
    response = client.get("/health")
    assert response.status_code == 200
    # HealthOut型の構造を確認（status, serviceが存在）
    json_data = response.json()
    assert "status" in json_data
    assert "service" in json_data

# TC5: 異常系 レスポンスモデル未指定の場合でも返却値が正しいか確認
def test_health_response_without_model():  # TC5
    # TC5: レスポンスモデル未指定の場合のテスト
    # FastAPIではエンドポイントのレスポンスモデルを外すには別途定義が必要
    # テスト用に直接関数を呼び出して確認
    from main import health  # health関数を直接インポート
    result = health()
    # HealthOut型インスタンスかどうか確認
    # 型名がHealthOutであることを確認
    assert hasattr(result, "status")
    assert hasattr(result, "service")
    assert result.status == "ok"
    assert result.service == "desk"

# TC6: 境界値テスト 他にパラメータがないため、正常系の境界値として確認
def test_health_get_boundary():  # TC6
    # TC6: GETリクエスト（境界値：パラメータなし）
    response = client.get("/health")
    assert response.status_code == 200

# TC7: 異常系 PUTリクエストでアクセスした場合、許可されていないメソッド
def test_health_put_method_not_allowed():  # TC7
    # TC7: PUTリクエスト
    response = client.put("/health")
    assert response.status_code == 405  # Method Not Allowed

# TC8: 異常系 DELETEリクエストでアクセスした場合、許可されていないメソッド
def test_health_delete_method_not_allowed():  # TC8
    # TC8: DELETEリクエスト
    response = client.delete("/health")
    assert response.status_code == 405  # Method Not Allowed

# TC9: 正常系 レスポンス内容が正しいか（statusとserviceの値が期待通りか）
def test_health_response_content():  # TC9
    # TC9: GETリクエスト
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert json_data["service"] == "desk"

# TC10: 正常系 レスポンスヘッダーがapplication/jsonであることを確認
def test_health_response_header_content_type():  # TC10
    # TC10: GETリクエスト
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

# TC11: 正常系 リクエストに余分なクエリパラメータが付与されていても正常応答すること
def test_health_get_with_extra_query_params():  # TC11
    # TC11: GETリクエスト（余分なクエリパラメータ付き）
    response = client.get("/health?foo=bar&baz=qux")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert json_data["service"] == "desk"

# TC12: 正常系 Acceptヘッダーがapplication/json以外でも正常応答すること
def test_health_get_with_non_json_accept_header():  # TC12
    # TC12: Acceptヘッダーをtext/htmlにしてGETリクエスト
    response = client.get("/health", headers={"Accept": "text/html"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert json_data["service"] == "desk"