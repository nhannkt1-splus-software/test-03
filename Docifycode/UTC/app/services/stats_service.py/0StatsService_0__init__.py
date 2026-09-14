import pytest

# ダミーのInMemoryStoreクラスを定義（テスト用）
class InMemoryStore:
    pass

# ダミーのオブジェクト用クラス（InMemoryStore以外）
class DummyStore:
    pass

from target import StatsService  # StatsServiceが定義されているモジュール名を'target'と仮定

# TC1: InMemoryStoreのインスタンスを渡した場合（正常系）
def test_stats_service_init_tc1():
    # テストID: TC1
    store = InMemoryStore()
    service = StatsService(store)
    assert service.store is store

# TC2: Noneを渡した場合（異常系）
def test_stats_service_init_tc2():
    # テストID: TC2
    store = None
    service = StatsService(store)
    assert service.store is None

# TC3: int型を渡した場合（異常系）
def test_stats_service_init_tc3():
    # テストID: TC3
    store = 123
    service = StatsService(store)
    assert service.store == 123

# TC4: str型を渡した場合（異常系）
def test_stats_service_init_tc4():
    # テストID: TC4
    store = 'store_string'
    service = StatsService(store)
    assert service.store == 'store_string'

# TC5: 空リストを渡した場合（異常系）
def test_stats_service_init_tc5():
    # テストID: TC5
    store = []
    service = StatsService(store)
    assert service.store == []

# TC6: 空辞書を渡した場合（異常系）
def test_stats_service_init_tc6():
    # テストID: TC6
    store = {}
    service = StatsService(store)
    assert service.store == {}

# TC7: ダミーのオブジェクトを渡した場合（異常系）
def test_stats_service_init_tc7():
    # テストID: TC7
    store = DummyStore()
    service = StatsService(store)
    assert service.store is store

# TC8: InMemoryStoreのインスタンスを渡してStatsServiceのインスタンスを生成するケース（正常系）
def test_stats_service_init_tc8():
    # テストID: TC8
    store = InMemoryStore()
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store is store

# TC9: Noneを渡してStatsServiceのインスタンスを生成するケース（異常系）
def test_stats_service_init_tc9():
    # テストID: TC9
    store = None
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store is None

# TC10: int型を渡してStatsServiceのインスタンスを生成するケース（異常系）
def test_stats_service_init_tc10():
    # テストID: TC10
    store = 123
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store == 123

# TC11: str型を渡してStatsServiceのインスタンスを生成するケース（異常系）
def test_stats_service_init_tc11():
    # テストID: TC11
    store = 'store_string'
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store == 'store_string'

# TC12: 空リストを渡してStatsServiceのインスタンスを生成するケース（異常系）
def test_stats_service_init_tc12():
    # テストID: TC12
    store = []
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store == []

# TC13: 空辞書を渡してStatsServiceのインスタンスを生成するケース（異常系）
def test_stats_service_init_tc13():
    # テストID: TC13
    store = {}
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store == {}

# TC14: ダミーのオブジェクトを渡してStatsServiceのインスタンスを生成するケース（異常系）
def test_stats_service_init_tc14():
    # テストID: TC14
    store = DummyStore()
    service = StatsService(store)
    assert isinstance(service, StatsService)
    assert service.store is store