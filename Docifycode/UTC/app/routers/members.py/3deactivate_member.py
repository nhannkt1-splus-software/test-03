import pytest

# テスト対象関数と依存関係をインポート
from fastapi import HTTPException, Depends
from your_module import deactivate_member, MemberOut, DeskError, http_error

# MemberServiceのモッククラス
class MockMemberService:
    def __init__(self, deactivate_behavior=None):
        self.deactivate_behavior = deactivate_behavior

    def deactivate(self, member_id):
        # TC1: 正常系（存在する会員ID）
        if self.deactivate_behavior == "success":
            # モックされたmemberオブジェクトを返す
            return {"id": member_id, "name": "Test Member"}
        # TC2, TC3, TC4: DeskError発生
        elif self.deactivate_behavior == "desk_error":
            raise DeskError("Member not found or invalid id")
        # その他は未定義

# get_member_serviceのモック
def get_mock_member_service_success():
    return MockMemberService(deactivate_behavior="success")

def get_mock_member_service_desk_error():
    return MockMemberService(deactivate_behavior="desk_error")

# pytestのfixtureで依存関係を差し替え
@pytest.fixture
def patch_depends(monkeypatch):
    # monkeypatchでDependsを無効化し、直接serviceを渡せるようにする
    monkeypatch.setattr("your_module.Depends", lambda x: x)

# TC1: 正常系：存在する会員IDを指定した場合
def test_deactivate_member_tc1(patch_depends):
    # テストID: TC1
    member_id = 1
    service = get_mock_member_service_success()
    result = deactivate_member(member_id, service)
    # MemberOutの検証
    assert isinstance(result, MemberOut)
    assert result.id == member_id
    assert result.name == "Test Member"

# TC2: 異常系：存在しない会員IDを指定した場合
def test_deactivate_member_tc2(patch_depends):
    # テストID: TC2
    member_id = 999999
    service = get_mock_member_service_desk_error()
    with pytest.raises(HTTPException):
        deactivate_member(member_id, service)

# TC3: 異常系：負の値の会員IDを指定した場合
def test_deactivate_member_tc3(patch_depends):
    # テストID: TC3
    member_id = -1
    service = get_mock_member_service_desk_error()
    with pytest.raises(HTTPException):
        deactivate_member(member_id, service)

# TC4: 異常系：0の会員IDを指定した場合
def test_deactivate_member_tc4(patch_depends):
    # テストID: TC4
    member_id = 0
    service = get_mock_member_service_desk_error()
    with pytest.raises(HTTPException):
        deactivate_member(member_id, service)

# TC5: 異常系：member_idが文字列型の場合（型不一致）
def test_deactivate_member_tc5(patch_depends):
    # テストID: TC5
    member_id = "abc"
    service = get_mock_member_service_success()
    with pytest.raises(TypeError):
        deactivate_member(member_id, service)

# TC6: 異常系：member_idがNoneの場合（型不一致）
def test_deactivate_member_tc6(patch_depends):
    # テストID: TC6
    member_id = None
    service = get_mock_member_service_success()
    with pytest.raises(TypeError):
        deactivate_member(member_id, service)

# TC7: 異常系：member_idがfloat型の場合（型不一致）
def test_deactivate_member_tc7(patch_depends):
    # テストID: TC7
    member_id = 1.5
    service = get_mock_member_service_success()
    with pytest.raises(TypeError):
        deactivate_member(member_id, service)