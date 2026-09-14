import pytest

# テスト用のダミーMemberクラスを定義
class Member:
    def __init__(self, username):
        self.username = username

# テスト対象のInMemoryStoreクラスをインポートまたは再定義
from types import SimpleNamespace

@pytest.fixture
def store_with_members():
    # テスト用のInMemoryStoreインスタンスを作成し、members属性をセット
    from __main__ import InMemoryStore  # テスト実行時に同一モジュール内にある前提
    store = InMemoryStore()
    # 既存ユーザー: alice, bob
    store.members = {
        1: Member("alice"),
        2: Member("bob"),
    }
    return store

# --- 正常系・大文字小文字区別しない一致 ---

# TC1: "alice"（小文字）で一致
def test_get_member_by_username_tc1(store_with_members):
    # TC1
    result = store_with_members.get_member_by_username("alice")
    # usernameが"alice"のMemberが返ること
    assert result is not None
    assert result.username == "alice"

# TC2: "ALICE"（大文字）で一致
def test_get_member_by_username_tc2(store_with_members):
    # TC2
    result = store_with_members.get_member_by_username("ALICE")
    assert result is not None
    assert result.username == "alice"

# TC3: "Alice"（先頭大文字）で一致
def test_get_member_by_username_tc3(store_with_members):
    # TC3
    result = store_with_members.get_member_by_username("Alice")
    assert result is not None
    assert result.username == "alice"

# TC4: "bob"（小文字）で一致
def test_get_member_by_username_tc4(store_with_members):
    # TC4
    result = store_with_members.get_member_by_username("bob")
    assert result is not None
    assert result.username == "bob"

# TC11: "ALICE"（大文字）で一致（重複パターン）
def test_get_member_by_username_tc11(store_with_members):
    # TC11
    result = store_with_members.get_member_by_username("ALICE")
    assert result is not None
    assert result.username == "alice"

# TC12: "Alice"（先頭大文字）で一致（重複パターン）
def test_get_member_by_username_tc12(store_with_members):
    # TC12
    result = store_with_members.get_member_by_username("Alice")
    assert result is not None
    assert result.username == "alice"

# TC13: "bob"（小文字）で一致（重複パターン）
def test_get_member_by_username_tc13(store_with_members):
    # TC13
    result = store_with_members.get_member_by_username("bob")
    assert result is not None
    assert result.username == "bob"

# --- 異常系・存在しないユーザー名 ---

# TC5: "charlie"（存在しないユーザー名）
def test_get_member_by_username_tc5(store_with_members):
    # TC5
    result = store_with_members.get_member_by_username("charlie")
    assert result is None

# TC14: "charlie"（存在しないユーザー名・重複パターン）
def test_get_member_by_username_tc14(store_with_members):
    # TC14
    result = store_with_members.get_member_by_username("charlie")
    assert result is None

# --- 異常系・空文字列 ---

# TC6: ""（空文字列）
def test_get_member_by_username_tc6(store_with_members):
    # TC6
    result = store_with_members.get_member_by_username("")
    assert result is None

# TC15: ""（空文字列・重複パターン）
def test_get_member_by_username_tc15(store_with_members):
    # TC15
    result = store_with_members.get_member_by_username("")
    assert result is None

# --- 異常系・型不一致 ---

# TC7: None型
def test_get_member_by_username_tc7(store_with_members):
    # TC7
    with pytest.raises(AttributeError):
        store_with_members.get_member_by_username(None)

# TC8: int型
def test_get_member_by_username_tc8(store_with_members):
    # TC8
    with pytest.raises(AttributeError):
        store_with_members.get_member_by_username(123)

# TC9: list型
def test_get_member_by_username_tc9(store_with_members):
    # TC9
    with pytest.raises(AttributeError):
        store_with_members.get_member_by_username([])

# TC16: None型（重複パターン）
def test_get_member_by_username_tc16(store_with_members):
    # TC16
    with pytest.raises(AttributeError):
        store_with_members.get_member_by_username(None)

# TC17: int型（重複パターン）
def test_get_member_by_username_tc17(store_with_members):
    # TC17
    with pytest.raises(AttributeError):
        store_with_members.get_member_by_username(123)

# TC18: list型（重複パターン）
def test_get_member_by_username_tc18(store_with_members):
    # TC18
    with pytest.raises(AttributeError):
        store_with_members.get_member_by_username([])

# --- 境界値テスト・100文字の長いユーザー名 ---

# TC10: 100文字の長いユーザー名（存在しない場合）
def test_get_member_by_username_tc10(store_with_members):
    # TC10
    long_username = "a" * 100
    result = store_with_members.get_member_by_username(long_username)
    assert result is None

# TC19: 100文字の長いユーザー名（存在しない場合・重複パターン）
def test_get_member_by_username_tc19(store_with_members):
    # TC19
    long_username = "a" * 100
    result = store_with_members.get_member_by_username(long_username)
    assert result is None