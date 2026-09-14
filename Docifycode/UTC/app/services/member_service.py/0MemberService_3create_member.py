import pytest

# テスト用のダミークラスと関数を定義
class InvalidUsernameError(Exception):
    pass

class DuplicateMemberError(Exception):
    pass

class Member:
    def __init__(self, username, display_name):
        self.username = username
        self.display_name = display_name

def normalize_username(username):
    # Noneや型違いの場合はTypeErrorを発生させる
    if username is None or not isinstance(username, str):
        raise TypeError("username must be a string")
    return username.strip()

def is_valid_username(username):
    # 空文字列や無効な文字を含む場合はFalse
    if not isinstance(username, str):
        return False
    if username == "":
        return False
    # 許可しない文字: 空白以外の記号
    import re
    if re.search(r"[^\w]", username):
        return False
    # 最小長: 1文字, 最大長: 100文字
    if len(username) < 1 or len(username) > 100:
        return False
    return True

class DummyStore:
    def __init__(self):
        self.members = {}

    def get_member_by_username(self, username):
        return self.members.get(username)

    def create_member(self, username, display_name):
        member = Member(username, display_name)
        self.members[username] = member
        return member

# MemberServiceのテスト用サブクラス
class MemberService:
    def __init__(self, store):
        self.store = store

    def create_member(self, username: str, display_name: str) -> Member:
        normalized = normalize_username(username)
        if not is_valid_username(normalized):
            raise InvalidUsernameError(username)
        if self.store.get_member_by_username(normalized):
            raise DuplicateMemberError(normalized)
        return self.store.create_member(normalized, display_name.strip())

# テスト用のfixture
@pytest.fixture
def member_service():
    return MemberService(DummyStore())

# --- TC1: 正常系：有効なユーザー名と表示名でメンバーが作成されるケース ---
def test_TC1_create_member_valid(member_service):
    # TC1
    member = member_service.create_member("valid_username", "valid_display_name")
    assert member.username == "valid_username"
    assert member.display_name == "valid_display_name"

# --- TC2: 正常系：ユーザー名に空白が含まれているが正規化後有効な場合 ---
def test_TC2_create_member_username_with_space(member_service):
    # TC2
    member = member_service.create_member(" valid_username ", "display_name")
    assert member.username == "valid_username"
    assert member.display_name == "display_name"

# --- TC3: 異常系：ユーザー名が無効な場合 ---
def test_TC3_create_member_invalid_username(member_service):
    # TC3
    with pytest.raises(InvalidUsernameError):
        member_service.create_member("invalid username!", "display_name")

# --- TC4: 異常系：ユーザー名が空文字列の場合 ---
def test_TC4_create_member_empty_username(member_service):
    # TC4
    with pytest.raises(InvalidUsernameError):
        member_service.create_member("", "display_name")

# --- TC5: 異常系：usernameがNone型の場合 ---
def test_TC5_create_member_username_none(member_service):
    # TC5
    with pytest.raises(TypeError):
        member_service.create_member(None, "display_name")

# --- TC6: 異常系：usernameがint型の場合 ---
def test_TC6_create_member_username_int(member_service):
    # TC6
    with pytest.raises(TypeError):
        member_service.create_member(123, "display_name")

# --- TC7: 異常系：既存ユーザー名の場合 ---
def test_TC7_create_member_duplicate_username(member_service):
    # TC7
    member_service.create_member("existing_username", "display_name")
    with pytest.raises(DuplicateMemberError):
        member_service.create_member("existing_username", "display_name")

# --- TC8: 境界値テスト：ユーザー名が最小長の場合 ---
def test_TC8_create_member_min_length_username(member_service):
    # TC8
    member = member_service.create_member("a", "display_name")
    assert member.username == "a"
    assert member.display_name == "display_name"

# --- TC9: 境界値テスト：ユーザー名が最大長の場合 ---
def test_TC9_create_member_max_length_username(member_service):
    # TC9
    username = "a" * 100
    member = member_service.create_member(username, "display_name")
    assert member.username == username
    assert member.display_name == "display_name"

# --- TC10: 正常系：display_nameに前後空白がある場合 ---
def test_TC10_create_member_display_name_with_space(member_service):
    # TC10
    member = member_service.create_member("valid_username", " display_name ")
    assert member.username == "valid_username"
    assert member.display_name == "display_name"

# --- TC11: 正常系：display_nameが空文字列の場合 ---
def test_TC11_create_member_display_name_empty(member_service):
    # TC11
    member = member_service.create_member("valid_username", "")
    assert member.username == "valid_username"
    assert member.display_name == ""

# --- TC12: 異常系：display_nameがNone型の場合 ---
def test_TC12_create_member_display_name_none(member_service):
    # TC12
    with pytest.raises(TypeError):
        member_service.create_member("valid_username", None)

# --- TC13: 異常系：display_nameがint型の場合 ---
def test_TC13_create_member_display_name_int(member_service):
    # TC13
    with pytest.raises(TypeError):
        member_service.create_member("valid_username", 123)

# --- TC14: 正常系：ユーザー名に空白を含み、display_nameが空文字列の場合 ---
def test_TC14_create_member_username_with_space_display_name_empty(member_service):
    # TC14
    member = member_service.create_member(" valid_username ", "")
    assert member.username == "valid_username"
    assert member.display_name == ""

# --- TC15: 正常系：ユーザー名に空白を含み、display_nameに前後空白がある場合 ---
def test_TC15_create_member_username_with_space_display_name_with_space(member_service):
    # TC15
    member = member_service.create_member(" valid_username ", " display_name ")
    assert member.username == "valid_username"
    assert member.display_name == "display_name"

# --- TC16: 境界値テスト：ユーザー名が最小長、display_nameが空文字列の場合 ---
def test_TC16_create_member_min_length_username_display_name_empty(member_service):
    # TC16
    member = member_service.create_member("a", "")
    assert member.username == "a"
    assert member.display_name == ""

# --- TC17: 境界値テスト：ユーザー名が最大長、display_nameが空文字列の場合 ---
def test_TC17_create_member_max_length_username_display_name_empty(member_service):
    # TC17
    username = "a" * 100
    member = member_service.create_member(username, "")
    assert member.username == username
    assert member.display_name == ""

# --- TC18: 境界値テスト：ユーザー名が最小長、display_nameに前後空白がある場合 ---
def test_TC18_create_member_min_length_username_display_name_with_space(member_service):
    # TC18
    member = member_service.create_member("a", " display_name ")
    assert member.username == "a"
    assert member.display_name == "display_name"

# --- TC19: 境界値テスト：ユーザー名が最大長、display_nameに前後空白がある場合 ---
def test_TC19_create_member_max_length_username_display_name_with_space(member_service):
    # TC19
    username = "a" * 100
    member = member_service.create_member(username, " display_name ")
    assert member.username == username
    assert member.display_name == "display_name"