import pytest

# テスト用のダミーTicketクラス
class Ticket:
    pass

# テスト対象のInMemoryStoreクラス
class InMemoryStore:
    """Process-local store. Enough for dummy CRUD and unit tests."""

    def __init__(self):
        # テスト用にtickets属性を初期化
        self.tickets = {}

    def get(self, ticket_id: int) -> Ticket | None:
        return self.tickets.get(ticket_id)

# -------------------------------
# 正常系・境界値・異常系テストケース
# -------------------------------

# TC1: 既存チケットID（1）を指定した場合
def test_get_existing_ticket_id_TC1():
    # チケットID 1 を登録
    store = InMemoryStore()
    store.tickets[1] = Ticket()
    # 期待値：Ticketインスタンス
    result = store.get(1)
    # Ticket型であることを確認
    assert isinstance(result, Ticket)

# TC2: 存在しないチケットID（999）を指定した場合
def test_get_non_existing_ticket_id_TC2():
    store = InMemoryStore()
    # 期待値：None
    result = store.get(999)
    assert result is None

# TC3: 境界値チケットID（0）を指定した場合
def test_get_boundary_ticket_id_zero_TC3():
    store = InMemoryStore()
    result = store.get(0)
    assert result is None

# TC4: 負のチケットID（-1）を指定した場合
def test_get_negative_ticket_id_TC4():
    store = InMemoryStore()
    result = store.get(-1)
    assert result is None

# TC5: 非常に大きいチケットID（1000000）を指定した場合
def test_get_large_ticket_id_TC5():
    store = InMemoryStore()
    result = store.get(1000000)
    assert result is None

# TC6: ticket_idがstr型（"1"）の場合
def test_get_ticket_id_str_TC6():
    store = InMemoryStore()
    # TypeErrorが発生することを期待
    with pytest.raises(TypeError):
        store.get("1")

# TC7: ticket_idがNone型の場合
def test_get_ticket_id_none_TC7():
    store = InMemoryStore()
    # TypeErrorが発生することを期待
    with pytest.raises(TypeError):
        store.get(None)

# TC8: ticket_idがfloat型（1.5）の場合
def test_get_ticket_id_float_TC8():
    store = InMemoryStore()
    # TypeErrorが発生することを期待
    with pytest.raises(TypeError):
        store.get(1.5)

# TC9: ticket_idがlist型（[]）の場合
def test_get_ticket_id_list_TC9():
    store = InMemoryStore()
    # TypeErrorが発生することを期待
    with pytest.raises(TypeError):
        store.get([])

# TC10: ticket_idがdict型（{}）の場合
def test_get_ticket_id_dict_TC10():
    store = InMemoryStore()
    # TypeErrorが発生することを期待
    with pytest.raises(TypeError):
        store.get({})

# TC11: int型の最大値（32bit）（2147483647）を指定した場合
def test_get_max_int_ticket_id_TC11():
    store = InMemoryStore()
    result = store.get(2147483647)
    assert result is None

# TC12: int型の最小値（32bit）（-2147483648）を指定した場合
def test_get_min_int_ticket_id_TC12():
    store = InMemoryStore()
    result = store.get(-2147483648)
    assert result is None