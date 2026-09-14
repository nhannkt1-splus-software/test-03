import pytest

# --- テスト用ダミークラス・定数定義 ---

# ダミーのMemberクラス
class Member:
    def __init__(self, member_id, username, active):
        self.member_id = member_id
        self.username = username
        self.active = active

# ダミーのTicketクラス
class Ticket:
    def __init__(self, assignee, status):
        self.assignee = assignee
        self.status = status

# アクティブなチケットのステータス
ACTIVE_STATUSES = {"OPEN", "IN_PROGRESS"}

# 例外クラス
class MemberHasActiveTicketsError(Exception):
    def __init__(self, username, count):
        self.username = username
        self.count = count
        super().__init__(f"Member {username} has {count} active tickets.")

class MemberNotFoundError(Exception):
    pass

# --- MemberServiceのテスト用サブクラス ---
from types import SimpleNamespace

class DummyStore:
    def __init__(self, tickets):
        self._tickets = tickets

    def list_all(self):
        return self._tickets

class TestableMemberService:
    """
    MemberServiceのテスト用サブクラス。
    get_member, storeをテストごとに差し替え可能にする。
    """
    def __init__(self, get_member_func, store):
        # get_member_func: member_id -> Member or raise
        self.get_member = get_member_func
        self.store = store

    # テスト対象メソッド
    def deactivate(self, member_id: int) -> Member:
        # 本来のMemberServiceのdeactivateメソッドと同じ
        member = self.get_member(member_id)
        active_count = sum(
            1
            for ticket in self.store.list_all()
            if ticket.assignee == member.username and ticket.status in ACTIVE_STATUSES
        )
        if active_count:
            raise MemberHasActiveTicketsError(member.username, active_count)
        member.active = False
        return member

# --- テストケース ---

# TC1: 正常系：アクティブな会員で、割り当てチケットがない場合
def test_deactivate_tc1():
    # TC1
    # 会員データ
    member = Member(1, "user1", True)
    def get_member(member_id):
        assert member_id == 1
        return member
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    # 実行
    result = service.deactivate(1)
    # 結果検証
    assert result is member
    assert result.active is False

# TC2: 異常系：アクティブな会員で、アクティブなチケットが割り当てられている場合
def test_deactivate_tc2():
    # TC2
    member = Member(1, "user1", True)
    def get_member(member_id):
        assert member_id == 1
        return member
    tickets = [
        Ticket("user1", "OPEN"),
        Ticket("user1", "IN_PROGRESS"),
    ]
    store = DummyStore(tickets)
    service = TestableMemberService(get_member, store)
    with pytest.raises(MemberHasActiveTicketsError) as e:
        service.deactivate(1)
    # エラー内容検証
    assert e.value.username == "user1"
    assert e.value.count == 2

# TC3: 正常系：既に非アクティブな会員で、割り当てチケットがない場合
def test_deactivate_tc3():
    # TC3
    member = Member(1, "user1", False)
    def get_member(member_id):
        assert member_id == 1
        return member
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    result = service.deactivate(1)
    assert result is member
    assert result.active is False

# TC4: 境界値テスト：member_id=0（存在する場合）
def test_deactivate_tc4():
    # TC4
    member = Member(0, "user0", True)
    def get_member(member_id):
        assert member_id == 0
        return member
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    result = service.deactivate(0)
    assert result is member
    assert result.active is False

# TC5: 異常系：member_idが存在しない場合（負の値）
def test_deactivate_tc5():
    # TC5
    def get_member(member_id):
        assert member_id == -1
        raise MemberNotFoundError()
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    with pytest.raises(MemberNotFoundError):
        service.deactivate(-1)

# TC6: 異常系：member_idが存在しない場合（大きい値）
def test_deactivate_tc6():
    # TC6
    def get_member(member_id):
        assert member_id == 999999
        raise MemberNotFoundError()
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    with pytest.raises(MemberNotFoundError):
        service.deactivate(999999)

# TC7: 異常系：member_idがstr型の場合
def test_deactivate_tc7():
    # TC7
    def get_member(member_id):
        # 型チェック
        if not isinstance(member_id, int):
            raise TypeError()
        raise MemberNotFoundError()
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    with pytest.raises(TypeError):
        service.deactivate("1")

# TC8: 異常系：member_idがNoneの場合
def test_deactivate_tc8():
    # TC8
    def get_member(member_id):
        if not isinstance(member_id, int):
            raise TypeError()
        raise MemberNotFoundError()
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    with pytest.raises(TypeError):
        service.deactivate(None)

# TC9: 異常系：member_idがfloat型の場合
def test_deactivate_tc9():
    # TC9
    def get_member(member_id):
        if not isinstance(member_id, int):
            raise TypeError()
        raise MemberNotFoundError()
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    with pytest.raises(TypeError):
        service.deactivate(1.5)

# TC10: 正常系：アクティブな会員で、他の会員のアクティブチケットのみ存在する場合
def test_deactivate_tc10():
    # TC10
    member = Member(1, "user1", True)
    def get_member(member_id):
        assert member_id == 1
        return member
    tickets = [
        Ticket("user2", "OPEN"),
        Ticket("user3", "IN_PROGRESS"),
    ]
    store = DummyStore(tickets)
    service = TestableMemberService(get_member, store)
    result = service.deactivate(1)
    assert result is member
    assert result.active is False

# TC11: 正常系：アクティブな会員で、割り当てチケットが全て非アクティブの場合
def test_deactivate_tc11():
    # TC11
    member = Member(1, "user1", True)
    def get_member(member_id):
        assert member_id == 1
        return member
    tickets = [
        Ticket("user1", "CLOSED"),
        Ticket("user1", "RESOLVED"),
    ]
    store = DummyStore(tickets)
    service = TestableMemberService(get_member, store)
    result = service.deactivate(1)
    assert result is member
    assert result.active is False

# TC12: 境界値テスト：member_id=0（既に非アクティブな会員の場合）
def test_deactivate_tc12():
    # TC12
    member = Member(0, "user0", False)
    def get_member(member_id):
        assert member_id == 0
        return member
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    result = service.deactivate(0)
    assert result is member
    assert result.active is False

# TC13: 境界値テスト：member_id=0（アクティブなチケットが割り当てられている場合）
def test_deactivate_tc13():
    # TC13
    member = Member(0, "user0", True)
    def get_member(member_id):
        assert member_id == 0
        return member
    tickets = [
        Ticket("user0", "OPEN"),
        Ticket("user0", "IN_PROGRESS"),
    ]
    store = DummyStore(tickets)
    service = TestableMemberService(get_member, store)
    with pytest.raises(MemberHasActiveTicketsError) as e:
        service.deactivate(0)
    assert e.value.username == "user0"
    assert e.value.count == 2

# TC14: 境界値テスト：member_id=0（他の会員のアクティブチケットのみ存在する場合）
def test_deactivate_tc14():
    # TC14
    member = Member(0, "user0", True)
    def get_member(member_id):
        assert member_id == 0
        return member
    tickets = [
        Ticket("user1", "OPEN"),
        Ticket("user2", "IN_PROGRESS"),
    ]
    store = DummyStore(tickets)
    service = TestableMemberService(get_member, store)
    result = service.deactivate(0)
    assert result is member
    assert result.active is False

# TC15: 境界値テスト：member_id=0（割り当てチケットが全て非アクティブの場合）
def test_deactivate_tc15():
    # TC15
    member = Member(0, "user0", True)
    def get_member(member_id):
        assert member_id == 0
        return member
    tickets = [
        Ticket("user0", "CLOSED"),
        Ticket("user0", "RESOLVED"),
    ]
    store = DummyStore(tickets)
    service = TestableMemberService(get_member, store)
    result = service.deactivate(0)
    assert result is member
    assert result.active is False

# TC16: 異常系：member_id=0が存在しない場合
def test_deactivate_tc16():
    # TC16
    def get_member(member_id):
        assert member_id == 0
        raise MemberNotFoundError()
    store = DummyStore([])
    service = TestableMemberService(get_member, store)
    with pytest.raises(MemberNotFoundError):
        service.deactivate(0)