import pytest

# Memberクラスのダミー定義
class Member:
    def __init__(self, id, active):
        self.id = id
        self.active = active

    def __eq__(self, other):
        return isinstance(other, Member) and self.id == other.id and self.active == other.active

    def __repr__(self):
        return f"Member(id={self.id}, active={self.active})"

# MemberServiceクラスのインポート（ここでは直接定義されているものと仮定）
from types import SimpleNamespace

@pytest.fixture
def member_service():
    # store属性を持つMemberServiceインスタンスを返す
    from __main__ import MemberService  # pytest実行時にスコープに入る想定
    service = MemberService()
    return service

# --- TC1: active=None, メンバー2件（active True/False） ---
def test_list_members_tc1(member_service):
    # TC1
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=False)]
    result = member_service.list_members(active=None)
    expected = [Member(id=1, active=True), Member(id=2, active=False)]
    assert result == expected  # 全件返す

# --- TC2: active=True, メンバー2件（active True/False） ---
def test_list_members_tc2(member_service):
    # TC2
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=False)]
    result = member_service.list_members(active=True)
    expected = [Member(id=1, active=True)]
    assert result == expected  # active=Trueのみ返す

# --- TC3: active=False, メンバー2件（active True/False） ---
def test_list_members_tc3(member_service):
    # TC3
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=False)]
    result = member_service.list_members(active=False)
    expected = [Member(id=2, active=False)]
    assert result == expected  # active=Falseのみ返す

# --- TC4: active=None, 空リスト ---
def test_list_members_tc4(member_service):
    # TC4
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: []
    result = member_service.list_members(active=None)
    expected = []
    assert result == expected  # 空リスト

# --- TC5: active=True, 空リスト ---
def test_list_members_tc5(member_service):
    # TC5
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: []
    result = member_service.list_members(active=True)
    expected = []
    assert result == expected  # 空リスト

# --- TC6: active=False, 空リスト ---
def test_list_members_tc6(member_service):
    # TC6
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: []
    result = member_service.list_members(active=False)
    expected = []
    assert result == expected  # 空リスト

# --- TC7: active=None, 全員active=True ---
def test_list_members_tc7(member_service):
    # TC7
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=True)]
    result = member_service.list_members(active=None)
    expected = [Member(id=1, active=True), Member(id=2, active=True)]
    assert result == expected  # 全件返す

# --- TC8: active=True, 全員active=True ---
def test_list_members_tc8(member_service):
    # TC8
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=True)]
    result = member_service.list_members(active=True)
    expected = [Member(id=1, active=True), Member(id=2, active=True)]
    assert result == expected  # 全件返す

# --- TC9: active=False, 全員active=True ---
def test_list_members_tc9(member_service):
    # TC9
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=True)]
    result = member_service.list_members(active=False)
    expected = []
    assert result == expected  # 該当なし

# --- TC10: active=None, 全員active=False ---
def test_list_members_tc10(member_service):
    # TC10
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=False), Member(id=2, active=False)]
    result = member_service.list_members(active=None)
    expected = [Member(id=1, active=False), Member(id=2, active=False)]
    assert result == expected  # 全件返す

# --- TC11: active=True, 全員active=False ---
def test_list_members_tc11(member_service):
    # TC11
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=False), Member(id=2, active=False)]
    result = member_service.list_members(active=True)
    expected = []
    assert result == expected  # 該当なし

# --- TC12: active=False, 全員active=False ---
def test_list_members_tc12(member_service):
    # TC12
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=False), Member(id=2, active=False)]
    result = member_service.list_members(active=False)
    expected = [Member(id=1, active=False), Member(id=2, active=False)]
    assert result == expected  # 全件返す

# --- TC13: active=1（int型）, 型不一致 ---
def test_list_members_tc13(member_service):
    # TC13
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=False)]
    with pytest.raises(TypeError):
        member_service.list_members(active=1)

# --- TC14: active="string"（str型）, 型不一致 ---
def test_list_members_tc14(member_service):
    # TC14
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=False)]
    with pytest.raises(TypeError):
        member_service.list_members(active="string")

# --- TC15: active=0.5（float型）, 型不一致 ---
def test_list_members_tc15(member_service):
    # TC15
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=1, active=True), Member(id=2, active=False)]
    with pytest.raises(TypeError):
        member_service.list_members(active=0.5)

# --- TC16: active=True, id順が逆のリスト ---
def test_list_members_tc16(member_service):
    # TC16
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=2, active=False), Member(id=1, active=True)]
    result = member_service.list_members(active=True)
    expected = [Member(id=1, active=True)]
    assert result == expected  # id昇順で返す

# --- TC17: active=False, id順が逆のリスト ---
def test_list_members_tc17(member_service):
    # TC17
    member_service.store = SimpleNamespace()
    member_service.store.list_members = lambda: [Member(id=2, active=False), Member(id=1, active=False)]
    result = member_service.list_members(active=False)
    expected = [Member(id=1, active=False), Member(id=2, active=False)]
    assert result == expected  # id昇順で返す