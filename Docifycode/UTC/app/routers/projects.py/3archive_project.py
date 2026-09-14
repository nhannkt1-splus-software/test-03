import pytest
from fastapi import HTTPException, Depends
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# テスト対象のFastAPI appをimport
from your_module import app  # ← your_moduleを実際のモジュール名に変更してください

# ProjectOut, DeskError, http_error, ProjectService, get_project_service もimport
from your_module import ProjectOut, DeskError

client = TestClient(app)

# --- 正常系: 存在するproject_idの場合 ---
# TC1
def test_TC1_archive_project_success(monkeypatch):
    # ProjectService.archiveのモック
    class DummyService:
        def archive(self, project_id):
            # project_id=1が正常
            return {"id": project_id, "name": "Test Project"}
    # ProjectOut.model_validateのモック
    monkeypatch.setattr("your_module.get_project_service", lambda: DummyService())
    # 実際のAPI呼び出し
    response = client.post("/1/archive")
    # 期待値: 200, 内容にid=1, name="Test Project"が含まれる
    assert response.status_code == 200  # 正常
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Project"

# --- 異常系: 存在しないproject_idの場合 ---
# TC2
def test_TC2_archive_project_not_found(monkeypatch):
    # ProjectService.archiveのモック
    class DummyService:
        def archive(self, project_id):
            raise DeskError("not found")
    monkeypatch.setattr("your_module.get_project_service", lambda: DummyService())
    response = client.post("/999999/archive")
    # 期待値: HTTPException (FastAPIは自動でHTTP 4xx/5xxを返す)
    assert response.status_code == 400 or response.status_code == 404

# --- 異常系: マイナス値のproject_idの場合 ---
# TC3
def test_TC3_archive_project_negative_id(monkeypatch):
    class DummyService:
        def archive(self, project_id):
            raise DeskError("invalid id")
    monkeypatch.setattr("your_module.get_project_service", lambda: DummyService())
    response = client.post("/-1/archive")
    assert response.status_code == 400 or response.status_code == 404

# --- 境界値: 0のproject_idの場合 ---
# TC4
def test_TC4_archive_project_zero_id(monkeypatch):
    class DummyService:
        def archive(self, project_id):
            raise DeskError("invalid id")
    monkeypatch.setattr("your_module.get_project_service", lambda: DummyService())
    response = client.post("/0/archive")
    assert response.status_code == 400 or response.status_code == 404

# --- 型不一致: 文字列型project_idの場合 ---
# TC5
def test_TC5_archive_project_string_id():
    # 文字列project_idはルーティングで404になる
    response = client.post("/abc/archive")
    # 期待値: 422 Unprocessable Entity または 404 Not Found
    assert response.status_code in (404, 422)

# --- 型不一致: Noneの場合 ---
# TC6
def test_TC6_archive_project_none_id():
    # NoneはURLで指定できないので、空文字列でテスト
    response = client.post("//archive")
    # 期待値: 404 Not Found
    assert response.status_code == 404

# --- 型不一致: float型project_idの場合 ---
# TC7
def test_TC7_archive_project_float_id():
    # float型project_idはルーティングで404になる
    response = client.post("/1.5/archive")
    # 期待値: 404 Not Found
    assert response.status_code == 404
```
**注記:**  
- `your_module` を実際の対象モジュール名に置き換えてください。
- `monkeypatch` を使って `get_project_service` を差し替えています。
- FastAPIのルーティング仕様上、int以外の型は404または422になります。
- `DeskError` 例外は400または404で返る想定です（実装により異なる場合は修正してください）。
- 各テストケースには日本語コメントでテストIDを明記しています。
