import pytest

# テスト用のダミーMemberクラス
class Member:
    def __init__(self, member_id):
        self.member_id = member_id

# テスト対象のInMemoryStoreクラスをインポートまたは定義済みと仮定
# members属性が存在しないため、テスト時に追加する

@pytest.fixture
def store():
    s = InMemoryStore()
    # members属性を初期化
    s.members = {}
    return s

# --- 正常系・境界値・異常系: membersに存在する場合 ---
# TC1: member_id=1, membersに存在する
def test_get_member_tc1(store):
    # TC1: 正常系
    # membersに1が存在する場合
    # 期待値: Memberインスタンスが返る
    store.members[1] = Member(1)
    result = store.get_member(1)
    assert isinstance(result, Member)  # TC1
    assert result.member_id == 1       # TC1

# TC3: member_id=0, membersに存在する
def test_get_member_tc3(store):
    # TC3: 境界値
    store.members[0] = Member(0)
    result = store.get_member(0)
    assert isinstance(result, Member)  # TC3
    assert result.member_id == 0       # TC3

# TC12: member_id=-1, membersに存在する
def test_get_member_tc12(store):
    # TC12: 異常系
    store.members[-1] = Member(-1)
    result = store.get_member(-1)
    assert isinstance(result, Member)  # TC12
    assert result.member_id == -1      # TC12

# TC13: member_id=999999999, membersに存在する
def test_get_member_tc13(store):
    # TC13: 異常系
    store.members[999999999] = Member(999999999)
    result = store.get_member(999999999)
    assert isinstance(result, Member)      # TC13
    assert result.member_id == 999999999   # TC13

# --- 正常系・境界値・異常系: membersに存在しない場合 ---
# TC2: member_id=2, membersに存在しない
def test_get_member_tc2(store):
    # TC2: 正常系
    result = store.get_member(2)
    assert result is None  # TC2

# TC4: member_id=0, membersに存在しない
def test_get_member_tc4(store):
    # TC4: 境界値
    result = store.get_member(0)
    assert result is None  # TC4

# TC5: member_id=-1, membersに存在しない
def test_get_member_tc5(store):
    # TC5: 異常系
    result = store.get_member(-1)
    assert result is None  # TC5

# TC6: member_id=999999999, membersに存在しない
def test_get_member_tc6(store):
    # TC6: 異常系
    result = store.get_member(999999999)
    assert result is None  # TC6

# --- 異常系: 型不正 ---
# TC7: member_id="1" (str型)
def test_get_member_tc7(store):
    # TC7: 異常系
    with pytest.raises(TypeError):  # TC7
        store.get_member("1")

# TC8: member_id=None (NoneType)
def test_get_member_tc8(store):
    # TC8: 異常系
    with pytest.raises(TypeError):  # TC8
        store.get_member(None)

# TC9: member_id=1.5 (float型)
def test_get_member_tc9(store):
    # TC9: 異常系
    with pytest.raises(TypeError):  # TC9
        store.get_member(1.5)

# TC10: member_id=[] (空リスト型)
def test_get_member_tc10(store):
    # TC10: 異常系
    with pytest.raises(TypeError):  # TC10
        store.get_member([])

# TC11: member_id={} (空辞書型)
def test_get_member_tc11(store):
    # TC11: 異常系
    with pytest.raises(TypeError):  # TC11
        store.get_member({})
```
