import pytest

# --- テスト用のダミークラス・関数定義 ---
# 本来は対象モジュールからimportするが、ここではテスト用にダミーを定義
class InMemoryStore:
    pass

class ProjectService:
    def __init__(self, store):
        # storeがInMemoryStoreまたはNone以外の場合TypeErrorを発生させる想定
        if not (isinstance(store, InMemoryStore) or store is None):
            raise TypeError("store must be InMemoryStore or None")
        self.store = store

def get_store():
    # デフォルトではInMemoryStoreインスタンスを返す
    return InMemoryStore()

# FastAPIのDependsのダミー
class Depends:
    def __init__(self, dependency):
        self.dependency = dependency

# テスト対象関数
def get_project_service(store: InMemoryStore = Depends(get_store)) -> ProjectService:
    return ProjectService(store)

# --- テストケース ---

# TC1: storeにInMemoryStoreインスタンスを渡した場合（正常系）
def test_get_project_service_tc1():
    # TC1
    store = InMemoryStore()
    service = get_project_service(store)
    # storeが正しくセットされていることを確認
    assert isinstance(service, ProjectService)
    assert service.store is store

# TC2: storeにNoneを渡した場合（正常系、ProjectServiceがNoneを許容する場合）
def test_get_project_service_tc2():
    # TC2
    store = None
    service = get_project_service(store)
    assert isinstance(service, ProjectService)
    assert service.store is None

# TC3: storeにint型（1）を渡した場合（異常系）
def test_get_project_service_tc3():
    # TC3
    store = 1
    with pytest.raises(TypeError):
        get_project_service(store)

# TC4: storeにstr型（'store'）を渡した場合（異常系）
def test_get_project_service_tc4():
    # TC4
    store = 'store'
    with pytest.raises(TypeError):
        get_project_service(store)

# TC5: storeにdict型（{}）を渡した場合（異常系）
def test_get_project_service_tc5():
    # TC5
    store = {}
    with pytest.raises(TypeError):
        get_project_service(store)

# TC6: Depends(get_store)で返却される値がstr型の場合（異常系）
def test_get_project_service_tc6(monkeypatch):
    # TC6
    def fake_get_store():
        return 'store'
    # monkeypatchでget_storeを置き換え
    monkeypatch.setattr(__name__ + ".get_store", fake_get_store)
    # Dependsの動作を模倣
    store = get_store()
    with pytest.raises(TypeError):
        get_project_service(store)

# TC7: partial applicationでInMemoryStoreインスタンスを渡した場合（正常系）
def test_get_project_service_tc7():
    # TC7
    from functools import partial
    store = InMemoryStore()
    func = partial(get_project_service, store)
    service = func()
    assert isinstance(service, ProjectService)
    assert service.store is store

# TC8: partial applicationでNoneを渡した場合（正常系）
def test_get_project_service_tc8():
    # TC8
    from functools import partial
    store = None
    func = partial(get_project_service, store)
    service = func()
    assert isinstance(service, ProjectService)
    assert service.store is None

# TC9: partial applicationでint型（1）を渡した場合（異常系）
def test_get_project_service_tc9():
    # TC9
    from functools import partial
    store = 1
    func = partial(get_project_service, store)
    with pytest.raises(TypeError):
        func()

# TC10: partial applicationでstr型（'store'）を渡した場合（異常系）
def test_get_project_service_tc10():
    # TC10
    from functools import partial
    store = 'store'
    func = partial(get_project_service, store)
    with pytest.raises(TypeError):
        func()

# TC11: partial applicationでdict型（{}）を渡した場合（異常系）
def test_get_project_service_tc11():
    # TC11
    from functools import partial
    store = {}
    func = partial(get_project_service, store)
    with pytest.raises(TypeError):
        func()
```
