import pytest

# Labelクラスのダミー定義（テスト用）
class Label:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# LabelServiceのテスト用ダミーstore
class DummyStore:
    def __init__(self, labels):
        self._labels = labels

    def list_labels(self):
        return self._labels

# テスト対象インスタンス生成ヘルパー
def make_service_with_labels(labels):
    service = LabelService()
    service.store = DummyStore(labels)
    return service

# id属性を持たないオブジェクト
class NoIdObject:
    pass

# --- 正常系 ---

# TC1, TC10: 空リスト
@pytest.mark.parametrize("test_id, labels", [
    ("TC1", []),
    ("TC10", []),
])
def test_list_labels_empty(test_id, labels):
    # テストID: test_id
    service = make_service_with_labels(labels)
    result = service.list_labels()
    assert result == []

# TC2, TC11: 要素1件
@pytest.mark.parametrize("test_id, labels", [
    ("TC2", [Label(id=1, name='A')]),
    ("TC11", [Label(id=1, name='A')]),
])
def test_list_labels_single(test_id, labels):
    # テストID: test_id
    service = make_service_with_labels(labels)
    result = service.list_labels()
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == 'A'

# TC3, TC12: 複数件・id順でない
@pytest.mark.parametrize("test_id, labels, expected_ids", [
    ("TC3", [Label(id=2, name='B'), Label(id=1, name='A')], [1,2]),
    ("TC12", [Label(id=2, name='B'), Label(id=1, name='A')], [1,2]),
])
def test_list_labels_multiple_unsorted(test_id, labels, expected_ids):
    # テストID: test_id
    service = make_service_with_labels(labels)
    result = service.list_labels()
    assert [label.id for label in result] == expected_ids

# TC4, TC13: id重複
@pytest.mark.parametrize("test_id, labels, expected_ids, expected_names", [
    ("TC4", [Label(id=1, name='A'), Label(id=1, name='B')], [1,1], ['A','B']),
    ("TC13", [Label(id=1, name='A'), Label(id=1, name='B')], [1,1], ['A','B']),
])
def test_list_labels_duplicate_id(test_id, labels, expected_ids, expected_names):
    # テストID: test_id
    service = make_service_with_labels(labels)
    result = service.list_labels()
    assert [label.id for label in result] == expected_ids
    assert [label.name for label in result] == expected_names

# TC5, TC14: 負数や0含む
@pytest.mark.parametrize("test_id, labels, expected_ids", [
    ("TC5", [Label(id=-1, name='X'), Label(id=0, name='Y'), Label(id=2, name='Z')], [-1,0,2]),
    ("TC14", [Label(id=-1, name='X'), Label(id=0, name='Y'), Label(id=2, name='Z')], [-1,0,2]),
])
def test_list_labels_negative_and_zero(test_id, labels, expected_ids):
    # テストID: test_id
    service = make_service_with_labels(labels)
    result = service.list_labels()
    assert [label.id for label in result] == expected_ids

# TC6, TC15: 非常に大きいid
@pytest.mark.parametrize("test_id, labels, expected_ids", [
    ("TC6", [Label(id=999999, name='max')], [999999]),
    ("TC15", [Label(id=999999, name='max')], [999999]),
])
def test_list_labels_large_id(test_id, labels, expected_ids):
    # テストID: test_id
    service = make_service_with_labels(labels)
    result = service.list_labels()
    assert [label.id for label in result] == expected_ids
    assert result[0].name == 'max'

# --- 異常系 ---

# TC7, TC16: 型不正な要素
@pytest.mark.parametrize("test_id, labels", [
    ("TC7", ['not_a_label', 123, None]),
    ("TC16", ['not_a_label', 123, None]),
])
def test_list_labels_invalid_type(test_id, labels):
    # テストID: test_id
    service = make_service_with_labels(labels)
    with pytest.raises(TypeError):
        service.list_labels()

# TC8, TC17: Noneが返る異常系
@pytest.mark.parametrize("test_id", [
    "TC8",
    "TC17",
])
def test_list_labels_none_returned(test_id):
    # テストID: test_id
    class StoreReturnsNone(DummyStore):
        def list_labels(self):
            return None
    service = LabelService()
    service.store = StoreReturnsNone(None)
    with pytest.raises(TypeError):
        service.list_labels()

# TC9, TC18: id属性を持たないオブジェクトを含むリスト
@pytest.mark.parametrize("test_id, labels", [
    ("TC9", [NoIdObject(), Label(id=1, name='A')]),
    ("TC18", [NoIdObject(), Label(id=1, name='A')]),
])
def test_list_labels_missing_id(test_id, labels):
    # テストID: test_id
    service = make_service_with_labels(labels)
    with pytest.raises(AttributeError):
        service.list_labels()