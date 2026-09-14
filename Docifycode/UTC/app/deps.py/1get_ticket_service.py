import pytest

# --- テスト用のダミークラスと関数を定義（本来はimportする） ---
class InMemoryStore:
    pass

class TicketService:
    def __init__(self, store):
        # storeがInMemoryStoreまたはNone以外の場合TypeErrorを発生させる仮定
        if store is not None and not isinstance(store, InMemoryStore):
            raise TypeError("store must be InMemoryStore or None")
        self.store = store

# get_storeは依存性注入用の関数
def get_store():
    return InMemoryStore()

# DependsはFastAPIの依存性注入用のダミー
class Depends:
    def __init__(self, func):
        self.func = func

# テスト対象関数
def get_ticket_service(store: InMemoryStore = Depends(get_store)) -> TicketService:
    # storeがDependsインスタンスの場合は、関数を呼び出して値を取得
    if isinstance(store, Depends):
        store = store.func()
    return TicketService(store)

# --- テストケース ---

# TC1: storeがInMemoryStoreのインスタンスの場合
def test_TC1_store_is_inmemorystore():
    # storeにInMemoryStoreのインスタンスを渡す
    store = InMemoryStore()
    # 例外が発生しないことを確認
    service = get_ticket_service(store)
    assert isinstance(service, TicketService)
    assert service.store is store  # storeがそのまま渡されていること

# TC2: storeがNoneの場合
def test_TC2_store_is_none():
    # storeにNoneを渡す
    service = get_ticket_service(None)
    assert isinstance(service, TicketService)
    assert service.store is None

# TC3: storeが整数値の場合（型不一致）
def test_TC3_store_is_int():
    # storeに整数値を渡すとTypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_ticket_service(1)

# TC4: storeが文字列の場合（型不一致）
def test_TC4_store_is_str():
    # storeに文字列を渡すとTypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_ticket_service('store')

# TC5: storeが空の辞書の場合（型不一致）
def test_TC5_store_is_dict():
    # storeに空の辞書を渡すとTypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_ticket_service({})

# TC6: get_store()がNoneを返す場合
def test_TC6_get_store_returns_none(monkeypatch):
    # get_store()がNoneを返すようにパッチ
    def fake_get_store():
        return None
    # store引数を省略し、Depends(get_store)が使われる
    service = get_ticket_service(Depends(fake_get_store))
    assert isinstance(service, TicketService)
    assert service.store is None

# TC7: get_store()がInMemoryStoreのインスタンスを返す場合
def test_TC7_get_store_returns_inmemorystore(monkeypatch):
    # get_store()がInMemoryStoreのインスタンスを返すようにパッチ
    def fake_get_store():
        return InMemoryStore()
    # store引数を省略し、Depends(fake_get_store)が使われる
    service = get_ticket_service(Depends(fake_get_store))
    assert isinstance(service, TicketService)
    assert isinstance(service.store, InMemoryStore)

# TC8: get_store()がNoneを返す場合、storeにもNoneを渡す
def test_TC8_store_and_get_store_none():
    # store=Depends(lambda: None)で両方None
    service = get_ticket_service(Depends(lambda: None))
    assert isinstance(service, TicketService)
    assert service.store is None

# TC9: get_store()が1を返す場合（型不一致）
def test_TC9_get_store_returns_int():
    # get_store()が1を返す場合、TypeErrorが発生することを確認
    def fake_get_store():
        return 1
    with pytest.raises(TypeError):
        get_ticket_service(Depends(fake_get_store))

# TC10: get_store()が'store'を返す場合（型不一致）
def test_TC10_get_store_returns_str():
    # get_store()が'store'を返す場合、TypeErrorが発生することを確認
    def fake_get_store():
        return 'store'
    with pytest.raises(TypeError):
        get_ticket_service(Depends(fake_get_store))

# TC11: get_store()が空の辞書を返す場合（型不一致）
def test_TC11_get_store_returns_dict():
    # get_store()が空の辞書を返す場合、TypeErrorが発生することを確認
    def fake_get_store():
        return {}
    with pytest.raises(TypeError):
        get_ticket_service(Depends(fake_get_store))