import pytest

# テスト対象のTicketService, InMemoryStoreをimport
# from your_module import TicketService, InMemoryStore

# --- TC1: storeにInMemoryStore型のインスタンスを渡した場合 ---
def test_service_with_inmemory_store_instance():
    # TC1
    store = InMemoryStore()
    try:
        service = TicketService(store)
    except Exception as e:
        pytest.fail(f"TC1: 例外が発生しました: {e}")

# --- TC2: storeにNoneを渡した場合 ---
def test_service_with_none_store():
    # TC2
    with pytest.raises(TypeError):
        TicketService(None)

# --- TC3: storeにint型を渡した場合 ---
def test_service_with_int_store():
    # TC3
    with pytest.raises(TypeError):
        TicketService(123)

# --- TC4: storeにstr型を渡した場合 ---
def test_service_with_str_store():
    # TC4
    with pytest.raises(TypeError):
        TicketService('store')

# --- TC5: storeに空リストを渡した場合 ---
def test_service_with_empty_list_store():
    # TC5
    with pytest.raises(TypeError):
        TicketService([])

# --- TC6: storeに空辞書を渡した場合 ---
def test_service_with_empty_dict_store():
    # TC6
    with pytest.raises(TypeError):
        TicketService({})

# --- TC7: storeにobject型のインスタンスを渡した場合 ---
def test_service_with_object_instance_store():
    # TC7
    with pytest.raises(TypeError):
        TicketService(object())

# --- TC8: storeにInMemoryStore型のインスタンスを渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_inmemory_store():
    # TC8
    from functools import partial
    store = InMemoryStore()
    try:
        service_factory = partial(TicketService, store)
        service = service_factory()
    except Exception as e:
        pytest.fail(f"TC8: 例外が発生しました: {e}")

# --- TC9: storeにNoneを渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_none_store():
    # TC9
    from functools import partial
    service_factory = partial(TicketService, None)
    with pytest.raises(TypeError):
        service_factory()

# --- TC10: storeにint型を渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_int_store():
    # TC10
    from functools import partial
    service_factory = partial(TicketService, 123)
    with pytest.raises(TypeError):
        service_factory()

# --- TC11: storeにstr型を渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_str_store():
    # TC11
    from functools import partial
    service_factory = partial(TicketService, 'store')
    with pytest.raises(TypeError):
        service_factory()

# --- TC12: storeに空リストを渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_empty_list_store():
    # TC12
    from functools import partial
    service_factory = partial(TicketService, [])
    with pytest.raises(TypeError):
        service_factory()

# --- TC13: storeに空辞書を渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_empty_dict_store():
    # TC13
    from functools import partial
    service_factory = partial(TicketService, {})
    with pytest.raises(TypeError):
        service_factory()

# --- TC14: storeにobject型のインスタンスを渡した場合の部分適用（partial application） ---
def test_service_partial_application_with_object_instance_store():
    # TC14
    from functools import partial
    service_factory = partial(TicketService, object())
    with pytest.raises(TypeError):
        service_factory()
```
