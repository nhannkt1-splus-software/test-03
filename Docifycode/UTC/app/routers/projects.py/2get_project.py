import pytest
from unittest.mock import MagicMock, patch
from fastapi import Depends
from fastapi.testclient import TestClient

# テスト対象のrouter, ProjectService, get_project_service, ProjectOut, DeskError, http_errorをimport
# ここでは仮のimport名とする。実際のパスに合わせて修正すること。
from your_module import router, ProjectService, get_project_service, ProjectOut, DeskError, http_error

# FastAPIのTestClientを利用
client = TestClient(router)

# ProjectOutのバリデーションエラー用
from pydantic import ValidationError

# --- テスト用のモックサービス定義 ---
class MockProjectService:
    def __init__(self, project=None, error=None):
        self.project = project
        self.error = error

    def get_project(self, project_id):
        if self.error:
            raise self.error
        return self.project

# --- ProjectOutのバリデーションを強制的に失敗させるためのヘルパー ---
class InvalidProject:
    pass

# --- 各テストケース ---

# TC1: 正常系: 存在するproject_id（int型）
def test_TC1_get_project_success(monkeypatch):
    # テストID: TC1
    project_data = {"id": 1, "name": "test"}  # ProjectOutが受け入れるdict
    mock_service = MockProjectService(project=project_data)
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    monkeypatch.setattr("your_module.ProjectOut.model_validate", classmethod(lambda cls, obj, from_attributes: ProjectOut(**obj)))
    response = client.get("/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# TC2: 正常系: 存在する大きなproject_id（int型）
def test_TC2_get_project_large_id(monkeypatch):
    # テストID: TC2
    project_data = {"id": 999999, "name": "bigproject"}
    mock_service = MockProjectService(project=project_data)
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    monkeypatch.setattr("your_module.ProjectOut.model_validate", classmethod(lambda cls, obj, from_attributes: ProjectOut(**obj)))
    response = client.get("/999999")
    assert response.status_code == 200
    assert response.json()["id"] == 999999

# TC3: 境界値: 0のproject_idが有効な場合
def test_TC3_get_project_id_zero_valid(monkeypatch):
    # テストID: TC3
    project_data = {"id": 0, "name": "zero"}
    mock_service = MockProjectService(project=project_data)
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    monkeypatch.setattr("your_module.ProjectOut.model_validate", classmethod(lambda cls, obj, from_attributes: ProjectOut(**obj)))
    response = client.get("/0")
    assert response.status_code == 200
    assert response.json()["id"] == 0

# TC4: 境界値: 0のproject_idが無効な場合（DeskError発生）
def test_TC4_get_project_id_zero_invalid(monkeypatch):
    # テストID: TC4
    mock_service = MockProjectService(error=DeskError("invalid id"))
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    # http_errorが例外を返すように
    monkeypatch.setattr("your_module.http_error", lambda exc: Exception("http error"))
    response = client.get("/0")
    assert response.status_code == 500 or response.status_code == 422 or response.status_code == 400

# TC5: 異常系: 負のproject_id（int型）
def test_TC5_get_project_negative_id(monkeypatch):
    # テストID: TC5
    mock_service = MockProjectService(error=DeskError("not found"))
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    monkeypatch.setattr("your_module.http_error", lambda exc: Exception("http error"))
    response = client.get("/-1")
    assert response.status_code == 500 or response.status_code == 422 or response.status_code == 400

# TC6: 型不一致: 文字列型project_id
def test_TC6_get_project_string_id():
    # テストID: TC6
    response = client.get("/abc")
    assert response.status_code == 422  # FastAPIのpath param型不一致は422

# TC7: 型不一致: None型project_id
def test_TC7_get_project_none_id():
    # テストID: TC7
    # NoneはURLで表現できないので、空パスでアクセス
    response = client.get("/")
    assert response.status_code == 404  # パスが一致しないため404

# TC8: 型不一致: float型project_id
def test_TC8_get_project_float_id():
    # テストID: TC8
    response = client.get("/1.5")
    assert response.status_code == 422  # FastAPIのpath param型不一致は422

# TC9: 型不一致: 空文字列project_id
def test_TC9_get_project_empty_string_id():
    # テストID: TC9
    response = client.get("//")
    assert response.status_code == 404  # パスが一致しないため404

# TC10: ProjectOut.model_validateでバリデーションエラーが発生する場合
def test_TC10_get_project_validation_error(monkeypatch):
    # テストID: TC10
    project_data = {"id": 1, "name": "test"}
    mock_service = MockProjectService(project=project_data)
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    # ProjectOut.model_validateがValidationErrorを投げるように
    def raise_validation_error(cls, obj, from_attributes):
        raise ValidationError([], ProjectOut)
    monkeypatch.setattr("your_module.ProjectOut.model_validate", classmethod(raise_validation_error))
    response = client.get("/1")
    assert response.status_code == 422 or response.status_code == 500

# TC11: ProjectOut.model_validateでバリデーションエラーが発生する場合（大きなproject_id）
def test_TC11_get_project_validation_error_large_id(monkeypatch):
    # テストID: TC11
    project_data = {"id": 999999, "name": "bigproject"}
    mock_service = MockProjectService(project=project_data)
    monkeypatch.setattr("your_module.get_project_service", lambda: mock_service)
    def raise_validation_error(cls, obj, from_attributes):
        raise ValidationError([], ProjectOut)
    monkeypatch.setattr("your_module.ProjectOut.model_validate", classmethod(raise_validation_error))
    response = client.get("/999999")
    assert response.status_code == 422 or response.status_code == 500