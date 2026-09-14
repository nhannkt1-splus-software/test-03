import pytest

# テスト対象関数をインポート
from target_module import test_health  # 'target_module'は実際のモジュール名に置き換えてください

from fastapi import FastAPI
from fastapi.testclient import TestClient

# --- TC1: 正常系：APIエンドポイントが正しく定義されている場合 ---
@pytest.fixture
def app_with_health():
    # /api/healthエンドポイントを持つFastAPIアプリ
    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app

# --- TC2: APIエンドポイントが存在しない場合 ---
@pytest.fixture
def app_without_health():
    # /api/healthエンドポイントを持たないFastAPIアプリ
    app = FastAPI()
    return app

# --- TC3: レスポンスに'status'キーが存在しない場合 ---
@pytest.fixture
def app_health_without_status():
    # /api/healthエンドポイントはあるが'status'キーがない
    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"message": "no status"}

    return app

# --- TC4: response.json()['status']が'ok'でない場合 ---
@pytest.fixture
def app_health_status_ng():
    # /api/healthエンドポイントはあるが'status'値が"ng"
    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"status": "ng"}

    return app

# --- TC1: 正常系 ---
def test_TC1_health_ok(app_with_health):
    # TC1: TestClientインスタンス # 正常なTestClientオブジェクト
    client = TestClient(app_with_health)
    # 期待される結果: None（assertに失敗しない）
    test_health(client)

# --- TC2: エンドポイントが存在しない場合 ---
def test_TC2_health_endpoint_not_found(app_without_health):
    # TC2: TestClientインスタンス（APIエンドポイントが存在しない場合）
    client = TestClient(app_without_health)
    # 期待される結果: AssertionError（status_codeが200でない）
    with pytest.raises(AssertionError):
        test_health(client)

# --- TC3: レスポンスに'status'キーが存在しない場合 ---
def test_TC3_health_status_key_missing(app_health_without_status):
    # TC3: TestClientインスタンス # response.json()に'status'キーが存在しない場合
    client = TestClient(app_health_without_status)
    # 期待される結果: KeyError
    with pytest.raises(KeyError):
        test_health(client)

# --- TC4: status値が期待値と異なる場合 ---
def test_TC4_health_status_not_ok(app_health_status_ng):
    # TC4: TestClientインスタンス # response.json()['status']が'ok'でない場合
    client = TestClient(app_health_status_ng)
    # 期待される結果: AssertionError
    with pytest.raises(AssertionError):
        test_health(client)

# --- TC5: clientがNoneの場合 ---
def test_TC5_client_is_none():
    # TC5: None # None型（型不一致）
    client = None
    # 期待される結果: AttributeError
    with pytest.raises(AttributeError):
        test_health(client)

# --- TC6: clientが整数値の場合 ---
def test_TC6_client_is_int():
    # TC6: 整数値1 # 型不一致
    client = 1
    # 期待される結果: AttributeError
    with pytest.raises(AttributeError):
        test_health(client)

# --- TC7: clientが文字列の場合 ---
def test_TC7_client_is_str():
    # TC7: 文字列'test' # 型不一致
    client = "test"
    # 期待される結果: AttributeError
    with pytest.raises(AttributeError):
        test_health(client)

# --- TC8: clientが辞書の場合 ---
def test_TC8_client_is_dict():
    # TC8: 空の辞書{} # 型不一致
    client = {}
    # 期待される結果: AttributeError
    with pytest.raises(AttributeError):
        test_health(client)