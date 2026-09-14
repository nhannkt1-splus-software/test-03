import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapi import Query
from fastapi.exceptions import RequestValidationError
from unittest.mock import patch, MagicMock
from typing import Any

# --- テスト用ダミー定義 ---
import sys

# ProjectOut, ProjectService, get_project_service, router をテスト用にimport
# 本来はテスト対象モジュールからimportする
# ここではテスト用ダミーを定義
class DummyProjectOut:
    def __init__(self, id, name, archived):
        self.id = id
        self.name = name
        self.archived = archived

    @classmethod
    def model_validate(cls, obj, from_attributes=False):
        # 型不正
        if isinstance(obj, Exception):
            raise obj
        # 値不正
        if isinstance(obj, dict) and obj.get("raise_value_error"):
            raise ValueError("Invalid value")
        # 型不正
        if not isinstance(obj, dict):
            raise TypeError("Invalid type")
        # 正常
        return cls(obj["id"], obj["name"], obj["archived"])

    def dict(self):
        return {"id": self.id, "name": self.name, "archived": self.archived}

# テスト対象のrouterをFastAPIにincludeする
from fastapi import APIRouter

router = APIRouter()

class DummyProjectService:
    def __init__(self, projects):
        self._projects = projects

    def list_projects(self, archived):
        return self._projects

def get_project_service_override(projects):
    def _get_service():
        return DummyProjectService(projects)
    return _get_service

# テスト対象のエンドポイントを再現
@router.get("", response_model=list[DummyProjectOut])
def list_projects(
    archived: bool | None = Query(default=None),
    service: DummyProjectService = Depends(get_project_service_override([])),
) -> list[DummyProjectOut]:
    return [
        DummyProjectOut.model_validate(project, from_attributes=True)
        for project in service.list_projects(archived)
    ]

# FastAPIアプリにルーターを追加
app = FastAPI()
app.include_router(router, prefix="/projects")

client = TestClient(app)

# --- テスト本体 ---

# ProjectOut, get_project_service, ProjectService をpatchする
@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    # ProjectOut
    monkeypatch.setitem(sys.modules, "ProjectOut", DummyProjectOut)
    # get_project_service
    monkeypatch.setitem(sys.modules, "get_project_service", get_project_service_override)
    # ProjectService
    monkeypatch.setitem(sys.modules, "ProjectService", DummyProjectService)

# --- 正常系 ---

# TC1: archived=None（未指定）で全プロジェクトを取得
def test_TC1_list_projects_all(monkeypatch):
    # テストデータ
    projects = [
        {"id": 1, "name": "A", "archived": False},
        {"id": 2, "name": "B", "archived": True},
    ]
    # 依存サービスを差し替え
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    # --- TC1 ---
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2

# TC2: archived=Trueでアーカイブ済みプロジェクトのみ取得
def test_TC2_list_projects_archived_true(monkeypatch):
    projects = [
        {"id": 2, "name": "B", "archived": True},
        {"id": 3, "name": "C", "archived": True},
    ]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    # --- TC2 ---
    response = client.get("/projects?archived=true")
    assert response.status_code == 200
    data = response.json()
    assert all(p["archived"] is True for p in data)

# TC3: archived=Falseでアーカイブされていないプロジェクトのみ取得
def test_TC3_list_projects_archived_false(monkeypatch):
    projects = [
        {"id": 1, "name": "A", "archived": False},
        {"id": 4, "name": "D", "archived": False},
    ]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    # --- TC3 ---
    response = client.get("/projects?archived=false")
    assert response.status_code == 200
    data = response.json()
    assert all(p["archived"] is False for p in data)

# TC4: archived=Noneで該当プロジェクトが存在しない場合
def test_TC4_list_projects_all_empty(monkeypatch):
    projects = []
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    # --- TC4 ---
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert data == []

# TC5: archived=True指定時に該当プロジェクトが存在しない場合
def test_TC5_list_projects_archived_true_empty(monkeypatch):
    projects = []
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    # --- TC5 ---
    response = client.get("/projects?archived=true")
    assert response.status_code == 200
    data = response.json()
    assert data == []

# TC6: archived=False指定時に該当プロジェクトが存在しない場合
def test_TC6_list_projects_archived_false_empty(monkeypatch):
    projects = []
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    # --- TC6 ---
    response = client.get("/projects?archived=false")
    assert response.status_code == 200
    data = response.json()
    assert data == []

# --- 型不一致バリデーションエラー ---

# TC7: archivedにstr型を指定した場合の型不一致エラー
def test_TC7_list_projects_archived_invalid_type_str():
    # --- TC7 ---
    response = client.get("/projects?archived=invalid_type")
    assert response.status_code == 422
    assert "value could not be parsed to a boolean" in response.text

# TC8: archivedにint型を指定した場合の型不一致エラー
def test_TC8_list_projects_archived_invalid_type_int():
    # --- TC8 ---
    response = client.get("/projects?archived=1")
    assert response.status_code == 422
    assert "value could not be parsed to a boolean" in response.text

# TC9: archivedにfloat型を指定した場合の型不一致エラー
def test_TC9_list_projects_archived_invalid_type_float():
    # --- TC9 ---
    response = client.get("/projects?archived=0.5")
    assert response.status_code == 422
    assert "value could not be parsed to a boolean" in response.text

# --- ProjectOut.model_validateで型不一致/値不正 ---

# TC10: service.list_projects(archived)の戻り値が不正な型の場合（TypeError）
def test_TC10_list_projects_invalid_type(monkeypatch):
    # --- TC10 ---
    projects = [object()]  # 型不正
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects")
    assert response.status_code == 500
    assert "Invalid type" in response.text

# TC11: service.list_projects(archived)の戻り値の値が不正な場合（ValueError）
def test_TC11_list_projects_invalid_value(monkeypatch):
    # --- TC11 ---
    projects = [{"id": 1, "name": "A", "archived": False, "raise_value_error": True}]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects")
    assert response.status_code == 500
    assert "Invalid value" in response.text

# TC12: archived=Trueでアーカイブ済みプロジェクトが複数件存在する場合
def test_TC12_list_projects_archived_true_multiple(monkeypatch):
    # --- TC12 ---
    projects = [
        {"id": 2, "name": "B", "archived": True},
        {"id": 3, "name": "C", "archived": True},
        {"id": 5, "name": "E", "archived": True},
    ]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects?archived=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(p["archived"] is True for p in data)

# TC13: archived=Falseでアーカイブされていないプロジェクトが1件のみ存在する場合
def test_TC13_list_projects_archived_false_single(monkeypatch):
    # --- TC13 ---
    projects = [
        {"id": 10, "name": "Z", "archived": False},
    ]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects?archived=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["archived"] is False

# TC14: archived=Noneで全プロジェクトが1件のみ存在する場合
def test_TC14_list_projects_all_single(monkeypatch):
    # --- TC14 ---
    projects = [
        {"id": 11, "name": "Y", "archived": True},
    ]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 11

# TC15: archived=True指定時、service.list_projects(archived)の戻り値が不正な型の場合（TypeError）
def test_TC15_list_projects_archived_true_invalid_type(monkeypatch):
    # --- TC15 ---
    projects = [object()]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects?archived=true")
    assert response.status_code == 500
    assert "Invalid type" in response.text

# TC16: archived=False指定時、service.list_projects(archived)の戻り値が不正な型の場合（TypeError）
def test_TC16_list_projects_archived_false_invalid_type(monkeypatch):
    # --- TC16 ---
    projects = [object()]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects?archived=false")
    assert response.status_code == 500
    assert "Invalid type" in response.text

# TC17: archived=True指定時、service.list_projects(archived)の戻り値の値が不正な場合（ValueError）
def test_TC17_list_projects_archived_true_invalid_value(monkeypatch):
    # --- TC17 ---
    projects = [{"id": 2, "name": "B", "archived": True, "raise_value_error": True}]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects?archived=true")
    assert response.status_code == 500
    assert "Invalid value" in response.text

# TC18: archived=False指定時、service.list_projects(archived)の戻り値の値が不正な場合（ValueError）
def test_TC18_list_projects_archived_false_invalid_value(monkeypatch):
    # --- TC18 ---
    projects = [{"id": 1, "name": "A", "archived": False, "raise_value_error": True}]
    app.dependency_overrides[get_project_service_override([])] = get_project_service_override(projects)
    response = client.get("/projects?archived=false")
    assert response.status_code == 500
    assert "Invalid value" in response.text