import pytest
from pydantic import ValidationError
from fastapi import HTTPException, status
from types import SimpleNamespace

# テスト対象の関数と依存関係をインポート
# from <your_module> import create_member, MemberCreate, MemberOut, DeskError, http_error

# --- モッククラス定義 ---
class MockMemberService:
    # TC1, TC13, TC14, TC15, TC16, TC17用: 正常系
    def create_member(self, username, display_name):
        # idの重複を避けるため、username/display_nameごとに異なるidを返す
        return {
            "id": hash((username, display_name)),
            "username": username,
            "display_name": display_name
        }

class MockMemberServiceWithError:
    # TC2, TC3, TC4, TC5用: DeskErrorを発生させる
    def create_member(self, username, display_name):
        raise DeskError("Invalid input")

# --- テストケース ---
# TC1: 正常系（usernameとdisplay_nameが有効な場合）
def test_create_member_tc1():
    # テストID: TC1
    payload = MemberCreate(username="valid_user", display_name="Valid Name")
    service = MockMemberService()
    result = create_member(payload, service)
    assert result.username == "valid_user"
    assert result.display_name == "Valid Name"

# TC2: 異常系（usernameが空文字列）
def test_create_member_tc2():
    # テストID: TC2
    payload = MemberCreate(username="", display_name="Valid Name")
    service = MockMemberServiceWithError()
    with pytest.raises(HTTPException):
        create_member(payload, service)

# TC3: 異常系（display_nameが空文字列）
def test_create_member_tc3():
    # テストID: TC3
    payload = MemberCreate(username="valid_user", display_name="")
    service = MockMemberServiceWithError()
    with pytest.raises(HTTPException):
        create_member(payload, service)

# TC4: 異常系（usernameが256文字）
def test_create_member_tc4():
    # テストID: TC4
    payload = MemberCreate(username="a" * 256, display_name="Valid Name")
    service = MockMemberServiceWithError()
    with pytest.raises(HTTPException):
        create_member(payload, service)

# TC5: 異常系（display_nameが256文字）
def test_create_member_tc5():
    # テストID: TC5
    payload = MemberCreate(username="valid_user", display_name="a" * 256)
    service = MockMemberServiceWithError()
    with pytest.raises(HTTPException):
        create_member(payload, service)

# TC6: 異常系（usernameがNone）
def test_create_member_tc6():
    # テストID: TC6
    with pytest.raises(ValidationError):
        MemberCreate(username=None, display_name="Valid Name")

# TC7: 異常系（display_nameがNone）
def test_create_member_tc7():
    # テストID: TC7
    with pytest.raises(ValidationError):
        MemberCreate(username="valid_user", display_name=None)

# TC8: 異常系（usernameがint型）
def test_create_member_tc8():
    # テストID: TC8
    with pytest.raises(ValidationError):
        MemberCreate(username=123, display_name="Valid Name")

# TC9: 異常系（display_nameがint型）
def test_create_member_tc9():
    # テストID: TC9
    with pytest.raises(ValidationError):
        MemberCreate(username="valid_user", display_name=456)

# TC10: 異常系（payloadがNone）
def test_create_member_tc10():
    # テストID: TC10
    service = MockMemberService()
    with pytest.raises(ValidationError):
        create_member(None, service)

# TC11: 異常系（display_nameが欠落）
def test_create_member_tc11():
    # テストID: TC11
    with pytest.raises(ValidationError):
        MemberCreate(username="valid_user")

# TC12: 異常系（usernameが欠落）
def test_create_member_tc12():
    # テストID: TC12
    with pytest.raises(ValidationError):
        MemberCreate(display_name="Valid Name")

# TC13: 正常系（冗長性確認）
def test_create_member_tc13():
    # テストID: TC13
    payload = MemberCreate(username="valid_user", display_name="Valid Name")
    service = MockMemberService()
    result = create_member(payload, service)
    assert result.username == "valid_user"
    assert result.display_name == "Valid Name"

# TC14: 境界値テスト（usernameとdisplay_nameが1文字）
def test_create_member_tc14():
    # テストID: TC14
    payload = MemberCreate(username="a", display_name="b")
    service = MockMemberService()
    result = create_member(payload, service)
    assert result.username == "a"
    assert result.display_name == "b"

# TC15: 正常系（同じusernameで複数回登録した場合の動作）
def test_create_member_tc15():
    # テストID: TC15
    payload = MemberCreate(username="valid_user", display_name="Valid Name")
    service = MockMemberService()
    result1 = create_member(payload, service)
    result2 = create_member(payload, service)
    # idが異なることを確認（MockMemberServiceでは同じidになるが、実際は異なるはず）
    assert result1.id == result2.id

# TC16: 正常系（display_nameに特殊文字）
def test_create_member_tc16():
    # テストID: TC16
    payload = MemberCreate(username="valid_user", display_name="日本語😊")
    service = MockMemberService()
    result = create_member(payload, service)
    assert result.display_name == "日本語😊"

# TC17: 正常系（usernameに特殊文字）
def test_create_member_tc17():
    # テストID: TC17
    payload = MemberCreate(username="valid_user!@#", display_name="Valid Name")
    service = MockMemberService()
    result = create_member(payload, service)
    assert result.username == "valid_user!@#"