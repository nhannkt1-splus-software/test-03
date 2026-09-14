import pytest

# テスト対象の関数・クラスをimport
from your_module import get_label_service, InMemoryStore, LabelService

# get_store, DependsはFastAPI等の依存性注入用のものなので、テストでは直接storeを渡す

# --- TC1: storeが正しい型の場合 ---
def test_get_label_service_with_valid_store_TC1():
    # TC1: InMemoryStoreのインスタンス
    store = InMemoryStore()
    # storeが正しい型の場合、LabelServiceのインスタンスが返ることを確認
    result = get_label_service(store)
    # 返り値がLabelServiceのインスタンスであること
    assert isinstance(result, LabelService)

# --- TC2: storeがNoneの場合 ---
def test_get_label_service_with_none_store_TC2():
    # TC2: storeがNone
    store = None
    # storeがNoneの場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store)

# --- TC3: storeがint型の場合 ---
def test_get_label_service_with_int_store_TC3():
    # TC3: storeがint型
    store = 1
    # storeがint型の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store)

# --- TC4: storeがstr型（空文字列）の場合 ---
def test_get_label_service_with_str_store_TC4():
    # TC4: storeがstr型（空文字列）
    store = ""
    # storeがstr型の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store)

# --- TC5: storeがlist型（空リスト）の場合 ---
def test_get_label_service_with_list_store_TC5():
    # TC5: storeがlist型（空リスト）
    store = []
    # storeがlist型の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store)

# --- TC6: storeが正しい型の場合（部分適用: storeのみ指定） ---
def test_get_label_service_with_valid_store_partial_TC6():
    # TC6: InMemoryStoreのインスタンス（部分適用: storeのみ指定）
    store = InMemoryStore()
    # storeが正しい型の場合、LabelServiceのインスタンスが返ることを確認
    result = get_label_service(store=store)
    # 返り値がLabelServiceのインスタンスであること
    assert isinstance(result, LabelService)

# --- TC7: storeがNoneの場合（部分適用: storeのみ指定） ---
def test_get_label_service_with_none_store_partial_TC7():
    # TC7: storeがNone（部分適用: storeのみ指定）
    store = None
    # storeがNoneの場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store=store)

# --- TC8: storeがint型の場合（部分適用: storeのみ指定） ---
def test_get_label_service_with_int_store_partial_TC8():
    # TC8: storeがint型（部分適用: storeのみ指定）
    store = 1
    # storeがint型の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store=store)

# --- TC9: storeがstr型（空文字列）の場合（部分適用: storeのみ指定） ---
def test_get_label_service_with_str_store_partial_TC9():
    # TC9: storeがstr型（空文字列）（部分適用: storeのみ指定）
    store = ""
    # storeがstr型の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store=store)

# --- TC10: storeがlist型（空リスト）の場合（部分適用: storeのみ指定） ---
def test_get_label_service_with_list_store_partial_TC10():
    # TC10: storeがlist型（空リスト）（部分適用: storeのみ指定）
    store = []
    # storeがlist型の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        get_label_service(store=store)