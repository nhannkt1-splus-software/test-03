import pytest

# TC1: 正常系: _storeが正常に返されるケース
def test_get_store_returns_store(monkeypatch):
    # _storeをダミーで定義
    class DummyStore:
        pass
    dummy_store = DummyStore()
    import sys

    # テスト対象関数が定義されているモジュールをimport
    import __main__ as target_module
    # _storeをモジュールにセット
    monkeypatch.setattr(target_module, "_store", dummy_store)
    # InMemoryStore型もダミーで定義
    monkeypatch.setattr(target_module, "InMemoryStore", DummyStore)

    # get_storeを取得
    get_store = getattr(target_module, "get_store")
    # _storeが返されることを確認
    assert get_store() is dummy_store

# TC2: _storeが未定義の場合の異常系: NameError例外が発生するケース
def test_get_store_raises_nameerror_when_store_undefined(monkeypatch):
    import sys
    import types

    # テスト対象関数が定義されているモジュールをimport
    import __main__ as target_module

    # _storeが存在する場合は削除
    if hasattr(target_module, "_store"):
        monkeypatch.delattr(target_module, "_store", raising=False)
    # InMemoryStore型もダミーで定義
    class DummyStore:
        pass
    monkeypatch.setattr(target_module, "InMemoryStore", DummyStore)

    # get_storeを取得
    get_store = getattr(target_module, "get_store")
    # _store未定義時にNameErrorが発生することを確認
    with pytest.raises(NameError):
        get_store()
```
