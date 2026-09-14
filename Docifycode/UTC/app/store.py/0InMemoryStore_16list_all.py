import pytest

# Ticketクラスのダミー定義（テスト用）
class Ticket:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __eq__(self, other):
        return isinstance(other, Ticket) and self.id == other.id and self.title == other.title

    def __repr__(self):
        return f"Ticket(id={self.id}, title={self.title!r})"

# InMemoryStoreクラスのダミー定義（テスト用）
class InMemoryStore:
    def list_all(self) -> list[Ticket]:
        return list(self.tickets.values())

# --- テストケース ---

# TC1: self.ticketsが空のdictの場合
def test_list_all_tc1():
    # self.ticketsを空dictに設定
    store = InMemoryStore()
    store.tickets = {}
    # 期待値: 空リスト
    assert store.list_all() == []

# TC2: self.ticketsに1件のTicketがある場合
def test_list_all_tc2():
    store = InMemoryStore()
    ticket1 = Ticket(id=1, title='test1')
    store.tickets = {'1': ticket1}
    # 期待値: 1件のTicketオブジェクトを含むリスト
    assert store.list_all() == [ticket1]

# TC3: self.ticketsに2件のTicketがある場合
def test_list_all_tc3():
    store = InMemoryStore()
    ticket1 = Ticket(id=1, title='test1')
    ticket2 = Ticket(id=2, title='test2')
    store.tickets = {'1': ticket1, '2': ticket2}
    # 期待値: 2件のTicketオブジェクトを含むリスト
    # dict.values()の順序は挿入順なので、[ticket1, ticket2]になる
    assert store.list_all() == [ticket1, ticket2]

# TC4: self.ticketsに100件のTicketがある場合（多件数・境界値）
def test_list_all_tc4():
    store = InMemoryStore()
    tickets_dict = {str(i): Ticket(id=i, title=f'test{i}') for i in range(1, 101)}
    store.tickets = tickets_dict
    expected = [Ticket(id=i, title=f'test{i}') for i in range(1, 101)]
    # 期待値: 100件のTicketオブジェクトを含むリスト
    assert store.list_all() == expected

# TC5: self.tickets属性が未定義の場合
def test_list_all_tc5():
    store = InMemoryStore()
    # self.tickets属性を定義しない
    # 期待値: AttributeError
    with pytest.raises(AttributeError):
        store.list_all()

# TC6: self.tickets属性がNoneの場合
def test_list_all_tc6():
    store = InMemoryStore()
    store.tickets = None
    # 期待値: TypeError（NoneTypeにvalues()は存在しない）
    with pytest.raises(TypeError):
        store.list_all()

# TC7: self.tickets属性がリスト型の場合
def test_list_all_tc7():
    store = InMemoryStore()
    store.tickets = []
    # 期待値: AttributeError（list型にvalues()は存在しない）
    with pytest.raises(AttributeError):
        store.list_all()
```
