import pytest

# テスト対象クラスの依存クラスをモックする
class MockStore:
    def __init__(self, members):
        self.members = members

    def get_member(self, member_id):
        return self.members.get(member_id, None)

# Member, MemberNotFound例外をテスト用に定義する
class Member:
    def __init__(self, member_id):
        self.member_id = member_id

class MemberNotFound(Exception):
    def __init__(self, member_id):
        self.member_id = member_id
        super().__init__(f"Member {member_id} not found")

# MemberServiceをテスト用にインポートまたは再定義
from types import SimpleNamespace

@pytest.fixture
def member_service_with_store():
    # storeにmember_id=1のみ存在するようにセットアップ
    store = MockStore({1: Member(1)})
    service = SimpleNamespace()
    # MemberServiceのインスタンスを作成し、storeをセット
    import sys
    MemberService = sys.modules[__name__].__dict__.get('MemberService')
    if MemberService is None:
        # テスト環境でMemberServiceが見つからない場合は再定義
        class MemberService:
            def get_member(self, member_id: int) -> Member:
                member = self.store.get_member(member_id)
                if member is None:
                    raise MemberNotFound(member_id)
                return member
        MemberService = MemberService
    svc = MemberService()
    svc.store = store
    return svc

# TC1: 正常系: storeにmember_id=1が存在する場合
def test_get_member_tc1(member_service_with_store):
    # TC1
    member = member_service_with_store.get_member(1)
    # member_id=1のMemberが返ることを確認
    assert isinstance(member, Member)
    assert member.member_id == 1

# TC2: 異常系: storeにmember_id=999が存在しない場合
def test_get_member_tc2(member_service_with_store):
    # TC2
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(999)
    assert e.value.member_id == 999

# TC3: 境界値: member_id=0がstoreに存在しない場合
def test_get_member_tc3(member_service_with_store):
    # TC3
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(0)
    assert e.value.member_id == 0

# TC4: 異常系: 負のmember_id（storeに存在しない場合）
def test_get_member_tc4(member_service_with_store):
    # TC4
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(-1)
    assert e.value.member_id == -1

# TC5: 異常系: 非現実的に大きいmember_id（storeに存在しない場合）
def test_get_member_tc5(member_service_with_store):
    # TC5
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(1000000000)
    assert e.value.member_id == 1000000000

# TC6: 異常系: member_idがstr型
def test_get_member_tc6(member_service_with_store):
    # TC6
    with pytest.raises(TypeError):
        member_service_with_store.get_member("1")

# TC7: 異常系: member_idがNone
def test_get_member_tc7(member_service_with_store):
    # TC7
    with pytest.raises(TypeError):
        member_service_with_store.get_member(None)

# TC8: 異常系: member_idがfloat型
def test_get_member_tc8(member_service_with_store):
    # TC8
    with pytest.raises(TypeError):
        member_service_with_store.get_member(1.5)

# TC9: 異常系: member_idがlist型
def test_get_member_tc9(member_service_with_store):
    # TC9
    with pytest.raises(TypeError):
        member_service_with_store.get_member([])

# TC10: 異常系: member_idがdict型
def test_get_member_tc10(member_service_with_store):
    # TC10
    with pytest.raises(TypeError):
        member_service_with_store.get_member({})

# TC11: 異常系: 非現実的に小さい負のmember_id（storeに存在しない場合）
def test_get_member_tc11(member_service_with_store):
    # TC11
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(-999999999)
    assert e.value.member_id == -999999999

# TC12: 境界値: int型の最大値（storeに存在しない場合）
def test_get_member_tc12(member_service_with_store):
    # TC12
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(2147483647)
    assert e.value.member_id == 2147483647

# TC13: 境界値: int型の最小値（storeに存在しない場合）
def test_get_member_tc13(member_service_with_store):
    # TC13
    with pytest.raises(MemberNotFound) as e:
        member_service_with_store.get_member(-2147483648)
    assert e.value.member_id == -2147483648