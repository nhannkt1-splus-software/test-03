import pytest

# テスト対象クラスのインスタンス生成用ヘルパー
def create_store_with_tickets(tickets_dict):
    store = InMemoryStore()
    store.tickets = tickets_dict.copy()
    return store

# TC1: ticketsに存在するキー(1)を削除するケース
def test_delete_TC1():
    # テストID: TC1
    store = create_store_with_tickets({1: "ticketA", 2: "ticketB"})
    store.delete(1)
    assert 1 not in store.tickets

# TC2: ticketsに存在しないキー(999)を指定した場合、何も起こらずNoneを返す
def test_delete_TC2():
    # テストID: TC2
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(999)
    assert store.tickets == {1: "ticketA"}

# TC3: 0がキーとして存在する場合の削除
def test_delete_TC3():
    # テストID: TC3
    store = create_store_with_tickets({0: "ticketZero", 1: "ticketA"})
    store.delete(0)
    assert 0 not in store.tickets

# TC4: 0がキーとして存在しない場合
def test_delete_TC4():
    # テストID: TC4
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(0)
    assert store.tickets == {1: "ticketA"}

# TC5: 負の整数で存在しないキー
def test_delete_TC5():
    # テストID: TC5
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(-1)
    assert store.tickets == {1: "ticketA"}

# TC6: 非常に大きな整数で存在しないキー
def test_delete_TC6():
    # テストID: TC6
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(1000000)
    assert store.tickets == {1: "ticketA"}

# TC7: str型のキー("1")。dictのキーとして存在しなければ何も起こらずNoneを返す
def test_delete_TC7():
    # テストID: TC7
    store = create_store_with_tickets({1: "ticketA"})
    store.delete("1")
    assert store.tickets == {1: "ticketA"}

# TC8: NoneType。dictのキーとして存在しない場合は何も起こらずNoneを返すが、型安全性の観点でTypeErrorが発生する可能性も考慮
def test_delete_TC8():
    # テストID: TC8
    store = create_store_with_tickets({1: "ticketA"})
    try:
        store.delete(None)
        # Noneがキーとして存在しない場合、例外は発生しない
        assert store.tickets == {1: "ticketA"}
    except TypeError:
        # TypeErrorが発生する場合も許容
        pass

# TC9: float型。dictのキーとして存在しなければ何も起こらずNoneを返す
def test_delete_TC9():
    # テストID: TC9
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(1.5)
    assert store.tickets == {1: "ticketA"}

# TC10: 空リスト型。listはdictのキーにできないためTypeErrorが発生
def test_delete_TC10():
    # テストID: TC10
    store = create_store_with_tickets({1: "ticketA"})
    with pytest.raises(TypeError):
        store.delete([])

# TC11: 空辞書型。dictはdictのキーにできないためTypeErrorが発生
def test_delete_TC11():
    # テストID: TC11
    store = create_store_with_tickets({1: "ticketA"})
    with pytest.raises(TypeError):
        store.delete({})

# TC12: bool型（True）はint型（1）と等価。ticketsに1が存在すれば削除、なければ何も起こらずNoneを返す
def test_delete_TC12():
    # テストID: TC12
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(True)
    assert 1 not in store.tickets

    # ticketsに1が存在しない場合
    store = create_store_with_tickets({2: "ticketB"})
    store.delete(True)
    assert store.tickets == {2: "ticketB"}

# TC13: bool型（False）はint型（0）と等価。ticketsに0が存在すれば削除、なければ何も起こらずNoneを返す
def test_delete_TC13():
    # テストID: TC13
    store = create_store_with_tickets({0: "ticketZero"})
    store.delete(False)
    assert 0 not in store.tickets

    # ticketsに0が存在しない場合
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(False)
    assert store.tickets == {1: "ticketA"}

# TC14: str型のキー("abc")。dictのキーとして存在しなければ何も起こらずNoneを返す
def test_delete_TC14():
    # テストID: TC14
    store = create_store_with_tickets({1: "ticketA"})
    store.delete("abc")
    assert store.tickets == {1: "ticketA"}

# TC15: NoneTypeがdictのキーとして存在する場合、削除され、例外は発生しない
def test_delete_TC15():
    # テストID: TC15
    store = create_store_with_tickets({None: "ticketNone", 1: "ticketA"})
    store.delete(None)
    assert None not in store.tickets
    assert 1 in store.tickets

# TC16: float型（1.0）はint型（1）と等価。ticketsに1が存在すれば削除、なければ何も起こらずNoneを返す
def test_delete_TC16():
    # テストID: TC16
    store = create_store_with_tickets({1: "ticketA"})
    store.delete(1.0)
    assert 1 not in store.tickets

    # ticketsに1が存在しない場合
    store = create_store_with_tickets({2: "ticketB"})
    store.delete(1.0)
    assert store.tickets == {2: "ticketB"}

# TC17: list型（複数要素）を指定した場合、TypeErrorが発生
def test_delete_TC17():
    # テストID: TC17
    store = create_store_with_tickets({1: "ticketA"})
    with pytest.raises(TypeError):
        store.delete([1, 2])

# TC18: dict型（要素あり）を指定した場合、TypeErrorが発生
def test_delete_TC18():
    # テストID: TC18
    store = create_store_with_tickets({1: "ticketA"})
    with pytest.raises(TypeError):
        store.delete({'a': 1})