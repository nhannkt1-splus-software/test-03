import pytest

# テスト対象クラスとMemberクラスの定義が必要
# Memberクラスのダミー定義（テスト用）
class Member:
    def __init__(self, id, username, display_name):
        self.id = id
        self.username = username
        self.display_name = display_name

# InMemoryStoreのダミー定義（テスト用）
class InMemoryStore:
    def __init__(self):
        self._next_member_id = 1
        self.members = {}

    def create_member(self, username: str, display_name: str) -> Member:
        if not isinstance(username, str):
            raise TypeError("username must be str")
        if not isinstance(display_name, str):
            raise TypeError("display_name must be str")
        member = Member(
            id=self._next_member_id,
            username=username,
            display_name=display_name,
        )
        self.members[member.id] = member
        self._next_member_id += 1
        return member

# --- 正常系・境界値・重複テスト ---

# TC1: 一般的な英数字の入力
def test_create_member_TC1():
    # テストID: TC1
    store = InMemoryStore()
    member = store.create_member("valid_username", "valid_display_name")
    assert isinstance(member, Member)
    assert member.username == "valid_username"
    assert member.display_name == "valid_display_name"
    assert member.id == 1

# TC2: usernameが空文字列
def test_create_member_TC2():
    # テストID: TC2
    store = InMemoryStore()
    member = store.create_member("", "valid_display_name")
    assert isinstance(member, Member)
    assert member.username == ""
    assert member.display_name == "valid_display_name"
    assert member.id == 1

# TC3: display_nameが空文字列
def test_create_member_TC3():
    # テストID: TC3
    store = InMemoryStore()
    member = store.create_member("valid_username", "")
    assert isinstance(member, Member)
    assert member.username == "valid_username"
    assert member.display_name == ""
    assert member.id == 1

# TC4: 両方空文字列
def test_create_member_TC4():
    # テストID: TC4
    store = InMemoryStore()
    member = store.create_member("", "")
    assert isinstance(member, Member)
    assert member.username == ""
    assert member.display_name == ""
    assert member.id == 1

# TC5: 日本語文字列
def test_create_member_TC5():
    # テストID: TC5
    store = InMemoryStore()
    member = store.create_member("ユーザー名", "表示名")
    assert isinstance(member, Member)
    assert member.username == "ユーザー名"
    assert member.display_name == "表示名"
    assert member.id == 1

# TC6: 特殊文字を含む文字列
def test_create_member_TC6():
    # テストID: TC6
    store = InMemoryStore()
    member = store.create_member("user!@#", "display$%^")
    assert isinstance(member, Member)
    assert member.username == "user!@#"
    assert member.display_name == "display$%^"
    assert member.id == 1

# TC7: 最大長の文字列（255文字）
def test_create_member_TC7():
    # テストID: TC7
    store = InMemoryStore()
    username = "a" * 255
    display_name = "b" * 255
    member = store.create_member(username, display_name)
    assert isinstance(member, Member)
    assert member.username == username
    assert member.display_name == display_name
    assert member.id == 1

# TC17: 両方空文字列（重複テスト）
def test_create_member_TC17():
    # テストID: TC17
    store = InMemoryStore()
    member = store.create_member("", "")
    assert isinstance(member, Member)
    assert member.username == ""
    assert member.display_name == ""
    assert member.id == 1

# --- 異常系 ---

# TC8: usernameがNone
def test_create_member_TC8():
    # テストID: TC8
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member(None, "valid_display_name")

# TC9: display_nameがNone
def test_create_member_TC9():
    # テストID: TC9
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member("valid_username", None)

# TC10: 両方None
def test_create_member_TC10():
    # テストID: TC10
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member(None, None)

# TC11: usernameがint型
def test_create_member_TC11():
    # テストID: TC11
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member(123, "valid_display_name")

# TC12: display_nameがint型
def test_create_member_TC12():
    # テストID: TC12
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member("valid_username", 456)

# TC13: usernameがリスト型（空リスト）
def test_create_member_TC13():
    # テストID: TC13
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member([], "valid_display_name")

# TC14: display_nameが辞書型（空辞書）
def test_create_member_TC14():
    # テストID: TC14
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member("valid_username", {})

# TC15: usernameが複数要素のリスト型
def test_create_member_TC15():
    # テストID: TC15
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member(["user1", "user2"], "valid_display_name")

# TC16: display_nameが値あり辞書型
def test_create_member_TC16():
    # テストID: TC16
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_member("valid_username", {"name": "display_name"})