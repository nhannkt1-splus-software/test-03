import pytest
from functools import partial

# --- テスト対象の依存クラス・関数のダミー定義 ---
# 本来はテスト対象モジュールからimportする
class InMemoryStore:
    pass

class MemberService:
    def __init__(self, store):
        # storeがNoneや不正な型の場合、例外を発生させる想定
        # ここでは型チェックや属性アクセスを仮定
        if store is None:
            # storeがNoneの場合、AttributeErrorを発生させる
            raise AttributeError("store is None")
        if not isinstance(store, InMemoryStore):
            # storeがInMemoryStoreでない場合、TypeErrorを発生させる
            raise TypeError("store must be InMemoryStore")
        self.store = store

def get_store():
    return InMemoryStore()

def get_member_service(store: InMemoryStore = get_store()):
    return MemberService(store)

# --- テストケース ---

# TC1: storeに正しい型のInMemoryStoreインスタンスを渡した場合
def test_get_member_service_tc1():
    # TC1
    store = InMemoryStore()
    # 正常にMemberServiceが返ることを確認
    service = get_member_service(store)
    assert isinstance(service, MemberService)
    assert service.store is store

# TC2: storeがNoneの場合、AttributeErrorが発生すること
def test_get_member_service_tc2():
    # TC2
    with pytest.raises(AttributeError):
        get_member_service(None)

# TC3: storeに整数型を渡した場合、TypeErrorが発生すること
def test_get_member_service_tc3():
    # TC3
    with pytest.raises(TypeError):
        get_member_service(123)

# TC4: storeに文字列型を渡した場合、TypeErrorが発生すること
def test_get_member_service_tc4():
    # TC4
    with pytest.raises(TypeError):
        get_member_service("store")

# TC5: storeに空の辞書型を渡した場合、TypeErrorが発生すること
def test_get_member_service_tc5():
    # TC5
    with pytest.raises(TypeError):
        get_member_service({})

# TC6: storeに未初期化のオブジェクトを渡した場合、AttributeErrorが発生すること
def test_get_member_service_tc6():
    # TC6
    class Dummy:
        pass
    dummy = object.__new__(Dummy)  # __init__が呼ばれていない未初期化オブジェクト
    with pytest.raises(AttributeError):
        get_member_service(dummy)

# TC7: partial applicationでInMemoryStoreインスタンスを渡した場合
def test_get_member_service_tc7():
    # TC7
    store = InMemoryStore()
    partial_func = partial(get_member_service, store)
    service = partial_func()
    assert isinstance(service, MemberService)
    assert service.store is store

# TC8: partial applicationでstoreがNoneの場合、AttributeErrorが発生すること
def test_get_member_service_tc8():
    # TC8
    partial_func = partial(get_member_service, None)
    with pytest.raises(AttributeError):
        partial_func()

# TC9: partial applicationでstoreに整数型を渡した場合、TypeErrorが発生すること
def test_get_member_service_tc9():
    # TC9
    partial_func = partial(get_member_service, 123)
    with pytest.raises(TypeError):
        partial_func()

# TC10: partial applicationでstoreに文字列型を渡した場合、TypeErrorが発生すること
def test_get_member_service_tc10():
    # TC10
    partial_func = partial(get_member_service, "store")
    with pytest.raises(TypeError):
        partial_func()

# TC11: partial applicationでstoreに空の辞書型を渡した場合、TypeErrorが発生すること
def test_get_member_service_tc11():
    # TC11
    partial_func = partial(get_member_service, {})
    with pytest.raises(TypeError):
        partial_func()

# TC12: partial applicationでstoreに未初期化のオブジェクトを渡した場合、AttributeErrorが発生すること
def test_get_member_service_tc12():
    # TC12
    class Dummy:
        pass
    dummy = object.__new__(Dummy)  # __init__が呼ばれていない未初期化オブジェクト
    partial_func = partial(get_member_service, dummy)
    with pytest.raises(AttributeError):
        partial_func()