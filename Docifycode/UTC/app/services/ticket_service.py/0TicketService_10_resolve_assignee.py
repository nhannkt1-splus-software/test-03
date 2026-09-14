import pytest

# テスト用の例外クラスを定義（本来は本体からimportする想定）
class MemberNotFound(Exception):
    pass

class MemberInactiveError(Exception):
    def __init__(self, username):
        self.username = username

# テスト用のモックメンバー
class MockMember:
    def __init__(self, username, active):
        self.username = username
        self.active = active

# テスト用のモックストア
class MockStore:
    def __init__(self):
        self.members = {}

    def get_member_by_username(self, username):
        return self.members.get(username, None)

# テスト対象クラスのimport（本来は本体からimportする想定）
from types import SimpleNamespace

# テスト対象クラスの定義（本来は本体からimportする想定）
class TicketService:
    def _resolve_assignee(self, username: str | None) -> str | None:
        if not username or not username.strip():
            return None
        member = self.store.get_member_by_username(username.strip())
        if member is None:
            raise MemberNotFound(username.strip())
        if not member.active:
            raise MemberInactiveError(member.username)
        return member.username

# テスト用のfixtureでTicketServiceインスタンスを生成
@pytest.fixture
def ticket_service():
    service = TicketService()
    service.store = MockStore()
    # 有効なユーザー
    service.store.members["valid_username"] = MockMember("valid_username", True)
    # 非アクティブユーザー
    service.store.members["inactive_username"] = MockMember("inactive_username", False)
    return service

# --- TC1: username=None ---
def test_resolve_assignee_none(ticket_service):
    # TC1: 入力がNoneの場合、Noneを返す
    assert ticket_service._resolve_assignee(None) is None

# --- TC2: username=""（空文字列） ---
def test_resolve_assignee_empty_string(ticket_service):
    # TC2: 入力が空文字列の場合、Noneを返す
    assert ticket_service._resolve_assignee("") is None

# --- TC3: username="   "（空白のみの文字列） ---
def test_resolve_assignee_spaces_only(ticket_service):
    # TC3: 入力が空白のみの文字列の場合、Noneを返す
    assert ticket_service._resolve_assignee("   ") is None

# --- TC4: username="valid_username"（有効なユーザー名） ---
def test_resolve_assignee_valid_username(ticket_service):
    # TC4: 有効なユーザー名で、メンバーがアクティブな場合
    assert ticket_service._resolve_assignee("valid_username") == "valid_username"

# --- TC5: username="nonexistent_username"（存在しないユーザー名） ---
def test_resolve_assignee_nonexistent_username(ticket_service):
    # TC5: 存在しないユーザー名の場合、MemberNotFound例外が発生する
    with pytest.raises(MemberNotFound):
        ticket_service._resolve_assignee("nonexistent_username")

# --- TC6: username="inactive_username"（非アクティブなユーザー名） ---
def test_resolve_assignee_inactive_username(ticket_service):
    # TC6: ユーザー名が存在するが非アクティブな場合、MemberInactiveError例外が発生する
    with pytest.raises(MemberInactiveError) as excinfo:
        ticket_service._resolve_assignee("inactive_username")
    # 例外のusername属性が正しいか確認
    assert getattr(excinfo.value, "username", None) == "inactive_username"

# --- TC7: username=123（int型） ---
def test_resolve_assignee_int_type(ticket_service):
    # TC7: 入力がint型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        ticket_service._resolve_assignee(123)

# --- TC8: username=[]（list型） ---
def test_resolve_assignee_list_type(ticket_service):
    # TC8: 入力がlist型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        ticket_service._resolve_assignee([])

# --- TC9: username={}（dict型） ---
def test_resolve_assignee_dict_type(ticket_service):
    # TC9: 入力がdict型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        ticket_service._resolve_assignee({})

# --- TC10: username=" valid_username "（前後に空白を含む有効なユーザー名） ---
def test_resolve_assignee_valid_username_with_spaces_1(ticket_service):
    # TC10: stripされて正常に返る
    assert ticket_service._resolve_assignee(" valid_username ") == "valid_username"

# --- TC11: username=" valid_username "（前後に空白を含む有効なユーザー名） ---
def test_resolve_assignee_valid_username_with_spaces_2(ticket_service):
    # TC11: stripされて正常に返る
    assert ticket_service._resolve_assignee(" valid_username ") == "valid_username"

# --- TC12: username=" valid_username "（前後に空白を含む有効なユーザー名） ---
def test_resolve_assignee_valid_username_with_spaces_3(ticket_service):
    # TC12: stripされて正常に返る
    assert ticket_service._resolve_assignee(" valid_username ") == "valid_username"
```
