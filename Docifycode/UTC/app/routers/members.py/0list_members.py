import pytest
from unittest.mock import MagicMock, patch
from fastapi import Query, Depends
from fastapi.testclient import TestClient

# テスト対象のFastAPIアプリとrouterをimport
from somewhere import app  # appのimportパスは実際のものに合わせて修正してください
from somewhere import MemberOut, get_member_service

client = TestClient(app)

# MemberServiceのモッククラス
class MockMemberService:
    def __init__(self, members):
        self._members = members

    def list_members(self, active):
        return self._members

# MemberOut.model_validateの正常系用ダミーデータ
def valid_member_dict():
    return {
        "id": 1,
        "name": "Taro",
        "active": True,
    }

# MemberOut.model_validateの属性不正用ダミーデータ
def invalid_member_dict():
    return {
        "id": 1,
        # "name"が欠落している
        "active": True,
    }

# get_member_serviceの依存性をモックに差し替えるfixture
@pytest.fixture
def patch_member_service(monkeypatch):
    def _patch(members):
        monkeypatch.setattr(
            "somewhere.get_member_service",
            lambda: MockMemberService(members)
        )
    return _patch

# MemberOut.model_validateをpatchするfixture
@pytest.fixture
def patch_model_validate(monkeypatch):
    def _patch(side_effect=None):
        monkeypatch.setattr(
            "somewhere.MemberOut.model_validate",
            MagicMock(side_effect=side_effect)
        )
    return _patch

# TC1: active=None（正常系）
def test_list_members_active_none_ok(patch_member_service):
    # TC1
    # メンバーが2人いる場合
    patch_member_service([valid_member_dict(), valid_member_dict()])
    response = client.get("/members")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2

# TC2: active=True（正常系）
def test_list_members_active_true_ok(patch_member_service):
    # TC2
    patch_member_service([valid_member_dict()])
    response = client.get("/members?active=true")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

# TC3: active=False（正常系）
def test_list_members_active_false_ok(patch_member_service):
    # TC3
    member = valid_member_dict()
    member["active"] = False
    patch_member_service([member])
    response = client.get("/members?active=false")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["active"] is False

# TC4: active=Trueで該当メンバーなし（正常系）
def test_list_members_active_true_empty(patch_member_service):
    # TC4
    patch_member_service([])
    response = client.get("/members?active=true")
    assert response.status_code == 200
    assert response.json() == []

# TC5: active=Falseで該当メンバーなし（正常系）
def test_list_members_active_false_empty(patch_member_service):
    # TC5
    patch_member_service([])
    response = client.get("/members?active=false")
    assert response.status_code == 200
    assert response.json() == []

# TC6: active=Noneでメンバー0人（正常系）
def test_list_members_active_none_empty(patch_member_service):
    # TC6
    patch_member_service([])
    response = client.get("/members")
    assert response.status_code == 200
    assert response.json() == []

# TC7: activeがbool型以外の文字列（異常系）
def test_list_members_active_invalid_type():
    # TC7
    response = client.get("/members?active=invalid_type")
    assert response.status_code == 422  # FastAPIのQueryパラメータ型不一致は422

# TC8: activeがint型（異常系）
def test_list_members_active_int():
    # TC8
    response = client.get("/members?active=1")
    assert response.status_code == 422  # bool型以外は422

# TC9: activeがfloat型（異常系）
def test_list_members_active_float():
    # TC9
    response = client.get("/members?active=0.5")
    assert response.status_code == 422  # bool型以外は422

# TC10: active=TrueでMemberOut.model_validateで属性不正（異常系）
def test_list_members_active_true_model_validate_error(patch_member_service, patch_model_validate):
    # TC10
    patch_member_service([invalid_member_dict()])
    from pydantic import ValidationError
    patch_model_validate(side_effect=ValidationError([], MemberOut))
    response = client.get("/members?active=true")
    assert response.status_code == 500 or response.status_code == 422  # FastAPIの例外ハンドリングによる

# TC11: active=NoneでMemberOut.model_validateで属性不正（異常系）
def test_list_members_active_none_model_validate_error(patch_member_service, patch_model_validate):
    # TC11
    patch_member_service([invalid_member_dict()])
    from pydantic import ValidationError
    patch_model_validate(side_effect=ValidationError([], MemberOut))
    response = client.get("/members")
    assert response.status_code == 500 or response.status_code == 422  # FastAPIの例外ハンドリングによる