import pytest

# テスト対象クラスのインポート
from target_module import InMemoryStore  # 実際のモジュール名に置き換えてください

# --- TC1: 正常系：InMemoryStoreインスタンス生成時に全ての属性が初期化され、例外が発生しないことを確認 ---
def test_TC1_inmemory_store_init_normal(monkeypatch):
    # _seed()が通常通り動作する場合
    # 何もモンキーパッチしない
    store = InMemoryStore()
    # 属性が空の辞書として初期化されていることを確認
    assert isinstance(store.tickets, dict)
    assert isinstance(store.members, dict)
    assert isinstance(store.projects, dict)
    assert isinstance(store.labels, dict)
    assert store.tickets == {}
    assert store.members == {}
    assert store.projects == {}
    assert store.labels == {}
    # IDカウンタも初期値
    assert store._next_ticket_id == 1
    assert store._next_member_id == 1
    assert store._next_project_id == 1
    assert store._next_label_id == 1

# --- TC2: 境界値：_seed()が初期データを投入しない場合でも、属性が空の状態で初期化されることを確認 ---
def test_TC2_inmemory_store_seed_empty(monkeypatch):
    # _seed()を空実装にモンキーパッチ
    monkeypatch.setattr(InMemoryStore, "_seed", lambda self: None)
    store = InMemoryStore()
    # 属性が空の辞書として初期化されていることを確認
    assert isinstance(store.tickets, dict)
    assert isinstance(store.members, dict)
    assert isinstance(store.projects, dict)
    assert isinstance(store.labels, dict)
    assert store.tickets == {}
    assert store.members == {}
    assert store.projects == {}
    assert store.labels == {}

# --- TC3: 境界値：_seed()が大量の初期データを投入しても、属性が正しく初期化されることを確認 ---
def test_TC3_inmemory_store_seed_many(monkeypatch):
    def many_seed(self):
        # 大量のダミーデータを投入
        self.tickets = {i: f"ticket{i}" for i in range(10000)}
        self.members = {i: f"member{i}" for i in range(10000)}
        self.projects = {i: f"project{i}" for i in range(10000)}
        self.labels = {i: f"label{i}" for i in range(10000)}
    monkeypatch.setattr(InMemoryStore, "_seed", many_seed)
    store = InMemoryStore()
    assert len(store.tickets) == 10000
    assert len(store.members) == 10000
    assert len(store.projects) == 10000
    assert len(store.labels) == 10000

# --- TC4: 異常系：_seed()が例外を発生させた場合、__init__も例外を伝播することを確認 ---
def test_TC4_inmemory_store_seed_raises(monkeypatch):
    def raise_seed(self):
        raise RuntimeError("seed error")
    monkeypatch.setattr(InMemoryStore, "_seed", raise_seed)
    with pytest.raises(RuntimeError) as excinfo:
        InMemoryStore()
    assert "seed error" in str(excinfo.value)

# --- TC5: 異常系：_seed()メソッドが存在しない場合、AttributeErrorが発生することを確認 ---
def test_TC5_inmemory_store_seed_missing(monkeypatch):
    # _seedを削除
    monkeypatch.delattr(InMemoryStore, "_seed", raising=False)
    with pytest.raises(AttributeError):
        InMemoryStore()

# --- TC6: 正常系：_seed()がNoneを返しても、__init__が正常に完了することを確認 ---
def test_TC6_inmemory_store_seed_returns_none(monkeypatch):
    monkeypatch.setattr(InMemoryStore, "_seed", lambda self: None)
    store = InMemoryStore()
    # 属性が空の辞書として初期化されていることを確認
    assert isinstance(store.tickets, dict)
    assert isinstance(store.members, dict)
    assert isinstance(store.projects, dict)
    assert isinstance(store.labels, dict)

# --- TC7: 境界値：_seed()が属性（tickets, members, projects, labels）を初期化しない場合でも、__init__で属性が空の辞書として初期化されることを確認 ---
def test_TC7_inmemory_store_seed_does_not_touch_attrs(monkeypatch):
    def noop_seed(self):
        # 属性に一切触れない
        pass
    monkeypatch.setattr(InMemoryStore, "_seed", noop_seed)
    store = InMemoryStore()
    assert isinstance(store.tickets, dict)
    assert isinstance(store.members, dict)
    assert isinstance(store.projects, dict)
    assert isinstance(store.labels, dict)
    assert store.tickets == {}
    assert store.members == {}
    assert store.projects == {}
    assert store.labels == {}

# --- TC8: 異常系：_seed()が属性（tickets, members, projects, labels）にNoneを代入しても、__init__が正常に完了することを確認 ---
def test_TC8_inmemory_store_seed_sets_none(monkeypatch):
    def none_seed(self):
        self.tickets = None
        self.members = None
        self.projects = None
        self.labels = None
    monkeypatch.setattr(InMemoryStore, "_seed", none_seed)
    store = InMemoryStore()
    assert store.tickets is None
    assert store.members is None
    assert store.projects is None
    assert store.labels is None

# --- TC9: 異常系：_seed()が属性（tickets, members, projects, labels）に不正な型（例：文字列）を代入しても、__init__が正常に完了することを確認 ---
def test_TC9_inmemory_store_seed_sets_invalid_type(monkeypatch):
    def invalid_seed(self):
        self.tickets = "not a dict"
        self.members = 123
        self.projects = [1, 2, 3]
        self.labels = (4, 5)
    monkeypatch.setattr(InMemoryStore, "_seed", invalid_seed)
    store = InMemoryStore()
    assert store.tickets == "not a dict"
    assert store.members == 123
    assert store.projects == [1, 2, 3]
    assert store.labels == (4, 5)

# --- TC10: 異常系：_seed()が属性（tickets, members, projects, labels）をdelで削除しても、__init__が正常に完了することを確認 ---
def test_TC10_inmemory_store_seed_deletes_attrs(monkeypatch):
    def del_seed(self):
        del self.tickets
        del self.members
        del self.projects
        del self.labels
    monkeypatch.setattr(InMemoryStore, "_seed", del_seed)
    store = InMemoryStore()
    # 属性が存在しないことを確認
    assert not hasattr(store, "tickets")
    assert not hasattr(store, "members")
    assert not hasattr(store, "projects")
    assert not hasattr(store, "labels")