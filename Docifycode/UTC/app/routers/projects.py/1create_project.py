import pytest
from unittest.mock import Mock, patch
from fastapi import Depends
from pydantic import ValidationError

# テスト対象関数のインポート
from your_module import create_project

# 必要な型や例外のインポート
from your_module import ProjectCreate, ProjectOut, ProjectService, DeskError, http_error

# ProjectCreateのバリデーションを直接テストするためのヘルパー
def make_project_create(data):
    return ProjectCreate(**data)

# ProjectServiceのモック作成
class MockProjectService:
    def __init__(self, create_project_side_effect=None, create_project_return=None):
        self.create_project_side_effect = create_project_side_effect
        self.create_project_return = create_project_return
        self.create_project_called_with = None

    def create_project(self, name, slug):
        self.create_project_called_with = (name, slug)
        if self.create_project_side_effect:
            raise self.create_project_side_effect
        return self.create_project_return

# ProjectOutのモックデータ
def make_project_out_dict(name="プロジェクトA", slug="project-a", id=1):
    return {"id": id, "name": name, "slug": slug}

# --- TC1: 正常系：有効なnameとslugでプロジェクト作成 ---
def test_create_project_tc1():
    # TC1
    payload = ProjectCreate(name="プロジェクトA", slug="project-a")
    project_dict = make_project_out_dict(name="プロジェクトA", slug="project-a")
    service = MockProjectService(create_project_return=project_dict)
    result = create_project(payload, service)
    assert isinstance(result, ProjectOut)
    assert result.name == "プロジェクトA"
    assert result.slug == "project-a"

# --- TC2: nameが空文字列 ---
def test_create_project_tc2():
    # TC2
    payload = ProjectCreate(name="", slug="project-a")
    service = MockProjectService(create_project_side_effect=DeskError("name is empty"))
    with pytest.raises(DeskError):
        create_project(payload, service)

# --- TC3: slugが空文字列 ---
def test_create_project_tc3():
    # TC3
    payload = ProjectCreate(name="プロジェクトA", slug="")
    service = MockProjectService(create_project_side_effect=DeskError("slug is empty"))
    with pytest.raises(DeskError):
        create_project(payload, service)

# --- TC4: nameが256文字の長い文字列 ---
def test_create_project_tc4():
    # TC4
    long_name = "a" * 256
    payload = ProjectCreate(name=long_name, slug="project-a")
    service = MockProjectService(create_project_side_effect=DeskError("name too long"))
    with pytest.raises(DeskError):
        create_project(payload, service)

# --- TC5: slugが256文字の長い文字列 ---
def test_create_project_tc5():
    # TC5
    long_slug = "a" * 256
    payload = ProjectCreate(name="プロジェクトA", slug=long_slug)
    service = MockProjectService(create_project_side_effect=DeskError("slug too long"))
    with pytest.raises(DeskError):
        create_project(payload, service)

# --- TC6: nameがnull ---
def test_create_project_tc6():
    # TC6
    data = {"name": None, "slug": "project-a"}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC7: slugがnull ---
def test_create_project_tc7():
    # TC7
    data = {"name": "プロジェクトA", "slug": None}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC8: nameがint型 ---
def test_create_project_tc8():
    # TC8
    data = {"name": 123, "slug": "project-a"}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC9: slugがint型 ---
def test_create_project_tc9():
    # TC9
    data = {"name": "プロジェクトA", "slug": 456}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC10: nameがリスト型 ---
def test_create_project_tc10():
    # TC10
    data = {"name": ["リスト"], "slug": "project-a"}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC11: slugがリスト型 ---
def test_create_project_tc11():
    # TC11
    data = {"name": "プロジェクトA", "slug": ["リスト"]}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC12: 空の辞書（必須フィールドなし） ---
def test_create_project_tc12():
    # TC12
    data = {}
    with pytest.raises(ValidationError):
        make_project_create(data)

# --- TC13: payloadがnull ---
def test_create_project_tc13():
    # TC13
    service = MockProjectService()
    with pytest.raises(TypeError):
        create_project(None, service)

# --- TC14: slug重複 ---
def test_create_project_tc14():
    # TC14
    payload = ProjectCreate(name="プロジェクトA", slug="project-a")
    service = MockProjectService(create_project_side_effect=DeskError("slug duplicated"))
    with pytest.raises(DeskError):
        create_project(payload, service)

# --- TC15: idが自動生成されることを確認するケース ---
def test_create_project_tc15():
    # TC15
    payload = ProjectCreate(name="プロジェクトA", slug="project-a")
    project_dict = make_project_out_dict(name="プロジェクトA", slug="project-a", id=123)
    service = MockProjectService(create_project_return=project_dict)
    result = create_project(payload, service)
    assert result.id == 123

# --- TC16: 戻り値がProjectOut型であることを確認するケース ---
def test_create_project_tc16():
    # TC16
    payload = ProjectCreate(name="プロジェクトA", slug="project-a")
    project_dict = make_project_out_dict(name="プロジェクトA", slug="project-a", id=999)
    service = MockProjectService(create_project_return=project_dict)
    result = create_project(payload, service)
    assert isinstance(result, ProjectOut)
```
