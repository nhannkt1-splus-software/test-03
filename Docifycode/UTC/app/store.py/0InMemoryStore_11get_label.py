import pytest

# テスト用のダミーLabelクラス
class Label:
    def __init__(self, label_id):
        self.label_id = label_id

# テスト対象のInMemoryStoreクラスをインポートまたは再定義
from target_module import InMemoryStore  # 実際のモジュール名に置き換えてください

@pytest.fixture
def store_with_labels():
    # テスト用のInMemoryStoreインスタンスを作成し、labels属性をセット
    store = InMemoryStore()
    # labels属性が存在しない場合は追加
    if not hasattr(store, 'labels'):
        store.labels = {}
    # label_id=1のみ存在させる
    store.labels[1] = Label(1)
    return store

# TC1: labelsに存在するlabel_idを指定した場合
def test_get_label_tc1(store_with_labels):
    # TC1
    # label_id=1はlabelsに存在する
    result = store_with_labels.get_label(1)
    assert isinstance(result, Label)
    assert result.label_id == 1

# TC2: labelsに存在しないlabel_idを指定した場合
def test_get_label_tc2(store_with_labels):
    # TC2
    # label_id=2はlabelsに存在しない
    result = store_with_labels.get_label(2)
    assert result is None

# TC3: labelsに存在しないlabel_id（境界値: 0）
def test_get_label_tc3(store_with_labels):
    # TC3
    # label_id=0はlabelsに存在しない
    result = store_with_labels.get_label(0)
    assert result is None

# TC4: labelsに存在しないlabel_id（負の値: -1）
def test_get_label_tc4(store_with_labels):
    # TC4
    # label_id=-1はlabelsに存在しない
    result = store_with_labels.get_label(-1)
    assert result is None

# TC5: labelsに存在しないlabel_id（大きな値: 999999）
def test_get_label_tc5(store_with_labels):
    # TC5
    # label_id=999999はlabelsに存在しない
    result = store_with_labels.get_label(999999)
    assert result is None

# TC6: label_idがstr型の場合
def test_get_label_tc6(store_with_labels):
    # TC6
    # label_id='1'（str型）はTypeErrorを期待
    with pytest.raises(TypeError):
        store_with_labels.get_label('1')

# TC7: label_idがNoneTypeの場合
def test_get_label_tc7(store_with_labels):
    # TC7
    # label_id=NoneはTypeErrorを期待
    with pytest.raises(TypeError):
        store_with_labels.get_label(None)

# TC8: label_idがfloat型の場合
def test_get_label_tc8(store_with_labels):
    # TC8
    # label_id=1.5（float型）はTypeErrorを期待
    with pytest.raises(TypeError):
        store_with_labels.get_label(1.5)

# TC9: label_idがlist型の場合
def test_get_label_tc9(store_with_labels):
    # TC9
    # label_id=[]（list型）はTypeErrorを期待
    with pytest.raises(TypeError):
        store_with_labels.get_label([])

# TC10: label_idがdict型の場合
def test_get_label_tc10(store_with_labels):
    # TC10
    # label_id={}（dict型）はTypeErrorを期待
    with pytest.raises(TypeError):
        store_with_labels.get_label({})

# TC11: int型の最大値（labelsに存在しない場合）
def test_get_label_tc11(store_with_labels):
    # TC11
    # label_id=2147483647（int型最大値）はlabelsに存在しない
    result = store_with_labels.get_label(2147483647)
    assert result is None

# TC12: int型の最小値（labelsに存在しない場合）
def test_get_label_tc12(store_with_labels):
    # TC12
    # label_id=-2147483648（int型最小値）はlabelsに存在しない
    result = store_with_labels.get_label(-2147483648)
    assert result is None