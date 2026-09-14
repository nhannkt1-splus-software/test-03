import pytest

# Labelクラスのダミー定義（テスト用）
class Label:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        # Label同士の比較用
        if not isinstance(other, Label):
            return False
        return self.id == other.id and self.name == other.name

    def __repr__(self):
        return f"Label(id={self.id!r}, name={self.name!r})"

# InMemoryStoreクラスのダミー定義（テスト用）
from types import SimpleNamespace

class InMemoryStore:
    """Process-local store. Enough for dummy CRUD and unit tests."""

    # テスト対象メソッド
    def list_labels(self) -> list[Label]:
        return list(self.labels.values())

# --- テストケース ---

# TC1: self.labelsが空のdictの場合
def test_list_labels_TC1():
    # self.labelsを空dictに設定
    store = InMemoryStore()
    store.labels = {}
    # 空リストが返ることを確認
    assert store.list_labels() == []

# TC2: self.labelsに1件のLabelオブジェクトがある場合
def test_list_labels_TC2():
    store = InMemoryStore()
    label = Label(id=1, name='test')
    store.labels = {1: label}
    # 1件のLabelが返ることを確認
    assert store.list_labels() == [label]

# TC3: self.labelsに複数件のLabelオブジェクトがある場合
def test_list_labels_TC3():
    store = InMemoryStore()
    label1 = Label(id=1, name='a')
    label2 = Label(id=2, name='b')
    store.labels = {1: label1, 2: label2}
    # 複数件のLabelが返ることを確認
    assert store.list_labels() == [label1, label2]

# TC4: self.labelsのキーがstr型でも値がLabelならリスト化される
def test_list_labels_TC4():
    store = InMemoryStore()
    label = Label(id='a', name='test')
    store.labels = {'a': label}
    # キーがstr型でも値がLabelならリスト化される
    assert store.list_labels() == [label]

# TC5: self.labelsの値がNoneの場合（異常系だが例外は発生しない）
def test_list_labels_TC5():
    store = InMemoryStore()
    store.labels = {1: None}
    # Noneがリストで返ることを確認
    assert store.list_labels() == [None]

# TC6: self.labels属性が未定義の場合（エラー系）
def test_list_labels_TC6():
    store = InMemoryStore()
    # self.labels属性を未定義のまま
    # AttributeErrorが発生することを確認
    with pytest.raises(AttributeError):
        store.list_labels()

# TC7: self.labelsがlist型などdict以外の場合（エラー系）
def test_list_labels_TC7():
    store = InMemoryStore()
    store.labels = []
    # AttributeErrorが発生することを確認
    with pytest.raises(AttributeError):
        store.list_labels()

# TC8: self.labelsがNoneの場合（エラー系）
def test_list_labels_TC8():
    store = InMemoryStore()
    store.labels = None
    # AttributeErrorが発生することを確認
    with pytest.raises(AttributeError):
        store.list_labels()

# TC9: self.labelsの値にnameが空文字のLabelが含まれる場合（正常系）
def test_list_labels_TC9():
    store = InMemoryStore()
    label1 = Label(id=1, name='')
    label2 = Label(id=2, name='b')
    store.labels = {1: label1, 2: label2}
    # nameが空文字のLabelもリスト化されることを確認
    assert store.list_labels() == [label1, label2]

# TC10: self.labelsの値にLabelとNoneが混在する場合（異常系だが例外は発生しない）
def test_list_labels_TC10():
    store = InMemoryStore()
    label1 = Label(id=1, name='test')
    store.labels = {1: label1, 2: None}
    # LabelとNoneが混在してリスト化されることを確認
    assert store.list_labels() == [label1, None]

# TC11: self.labelsの値にLabel以外（str型）が含まれる場合（異常系だが例外は発生しない）
def test_list_labels_TC11():
    store = InMemoryStore()
    label1 = Label(id=1, name='test')
    store.labels = {1: label1, 2: 'not a Label'}
    # Labelとstr型が混在してリスト化されることを確認
    assert store.list_labels() == [label1, 'not a Label']

# TC12: self.labelsの値がint型の場合（異常系だが例外は発生しない）
def test_list_labels_TC12():
    store = InMemoryStore()
    store.labels = {1: 123, 2: 456}
    # int型がリスト化されることを確認
    assert store.list_labels() == [123, 456]

# TC13: self.labelsの値にLabelとdict型が混在する場合（異常系だが例外は発生しない）
def test_list_labels_TC13():
    store = InMemoryStore()
    label1 = Label(id=1, name='test')
    dict_label = {'id': 2, 'name': 'b'}
    store.labels = {1: label1, 2: dict_label}
    # Labelとdict型が混在してリスト化されることを確認
    assert store.list_labels() == [label1, dict_label]