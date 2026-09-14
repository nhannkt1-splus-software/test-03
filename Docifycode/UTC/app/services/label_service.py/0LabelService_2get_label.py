import pytest

# テスト用のダミークラスと例外を定義
class Label:
    def __init__(self, label_id):
        self.label_id = label_id

class LabelNotFound(Exception):
    def __init__(self, label_id):
        self.label_id = label_id
        super().__init__(f"Label not found: {label_id}")

# テスト用のダミーストア
class DummyStore:
    def __init__(self, labels):
        self.labels = labels

    def get_label(self, label_id):
        return self.labels.get(label_id, None)

# テスト対象のLabelServiceを初期化するヘルパー
def create_label_service(labels_dict):
    service = LabelService()
    service.store = DummyStore(labels_dict)
    return service

# --- TC1: 正常系: 存在するラベルIDを指定した場合 ---
def test_get_label_TC1():
    # label_id=1が存在する場合
    service = create_label_service({1: Label(1)})
    # 期待値: Labelインスタンスが返る
    result = service.get_label(1)
    assert isinstance(result, Label)
    assert result.label_id == 1

# --- TC2: 異常系: 存在しないラベルIDを指定した場合 ---
def test_get_label_TC2():
    # label_id=9999が存在しない場合
    service = create_label_service({})
    # 期待値: LabelNotFound例外が発生
    with pytest.raises(LabelNotFound) as e:
        service.get_label(9999)
    assert e.value.label_id == 9999

# --- TC3: 境界値: 0番のラベルが存在する場合 ---
def test_get_label_TC3():
    # label_id=0が存在する場合
    service = create_label_service({0: Label(0)})
    # 期待値: Labelインスタンスが返る
    result = service.get_label(0)
    assert isinstance(result, Label)
    assert result.label_id == 0

# --- TC4: 境界値: 0番のラベルが存在しない場合 ---
def test_get_label_TC4():
    # label_id=0が存在しない場合
    service = create_label_service({})
    # 期待値: LabelNotFound例外が発生
    with pytest.raises(LabelNotFound) as e:
        service.get_label(0)
    assert e.value.label_id == 0

# --- TC5: 異常系: 負のラベルIDを指定した場合 ---
def test_get_label_TC5():
    # label_id=-1が存在しない場合
    service = create_label_service({})
    # 期待値: LabelNotFound例外が発生
    with pytest.raises(LabelNotFound) as e:
        service.get_label(-1)
    assert e.value.label_id == -1

# --- TC6: 異常系: label_idがstr型の場合 ---
def test_get_label_TC6():
    service = create_label_service({})
    # 期待値: TypeError例外が発生
    with pytest.raises(TypeError):
        service.get_label("abc")

# --- TC7: 異常系: label_idがNoneTypeの場合 ---
def test_get_label_TC7():
    service = create_label_service({})
    # 期待値: TypeError例外が発生
    with pytest.raises(TypeError):
        service.get_label(None)

# --- TC8: 異常系: label_idがfloat型の場合 ---
def test_get_label_TC8():
    service = create_label_service({})
    # 期待値: TypeError例外が発生
    with pytest.raises(TypeError):
        service.get_label(1.5)

# --- TC9: 異常系: label_idがlist型の場合 ---
def test_get_label_TC9():
    service = create_label_service({})
    # 期待値: TypeError例外が発生
    with pytest.raises(TypeError):
        service.get_label([])

# --- TC10: 異常系: label_idがdict型の場合 ---
def test_get_label_TC10():
    service = create_label_service({})
    # 期待値: TypeError例外が発生
    with pytest.raises(TypeError):
        service.get_label({})

# --- TC11: 異常系: 非常に大きいラベルIDを指定した場合、存在しない場合 ---
def test_get_label_TC11():
    # label_id=1000000が存在しない場合
    service = create_label_service({})
    # 期待値: LabelNotFound例外が発生
    with pytest.raises(LabelNotFound) as e:
        service.get_label(1000000)
    assert e.value.label_id == 1000000

# --- TC12: 異常系: 非常に小さい負のラベルIDを指定した場合、存在しない場合 ---
def test_get_label_TC12():
    # label_id=-1000000が存在しない場合
    service = create_label_service({})
    # 期待値: LabelNotFound例外が発生
    with pytest.raises(LabelNotFound) as e:
        service.get_label(-1000000)
    assert e.value.label_id == -1000000