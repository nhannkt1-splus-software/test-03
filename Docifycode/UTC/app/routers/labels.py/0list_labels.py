import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from pydantic import ValidationError
from types import SimpleNamespace

# --- テスト対象関数の依存関係を模擬するためのヘルパー ---
# LabelOut, LabelService, get_label_service, router をインポートまたはモックする必要があります
# ここではテストのためにモックを作成します

# LabelOutのモック（実際の属性に合わせて調整してください）
class LabelOut:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def model_validate(cls, obj, from_attributes=False):
        # 属性値のバリデーション（簡易版）
        if not hasattr(obj, 'id') or not hasattr(obj, 'name'):
            raise ValidationError("属性欠損")
        if obj.id is None or obj.name is None:
            raise ValidationError("属性欠損")
        if not isinstance(obj.id, int):
            raise ValidationError("id型不正")
        if not isinstance(obj.name, str):
            raise ValidationError("name型不正")
        if obj.name == "":
            raise ValidationError("name空文字")
        return cls(obj.id, obj.name)

# LabelServiceのモック
class MockLabelService:
    def __init__(self, return_value=None, raise_exception=None):
        self.return_value = return_value
        self.raise_exception = raise_exception

    def list_labels(self):
        if self.raise_exception:
            raise self.raise_exception
        return self.return_value

# get_label_serviceのモック
def get_label_service_mock(service):
    return lambda: service

# テスト対象関数の直接呼び出し
def list_labels(service):
    return [
        LabelOut.model_validate(label, from_attributes=True) for label in service.list_labels()
    ]

# --- テストケース ---
# TC1: ラベルが存在しない場合（空リスト）
def test_TC1_list_labels_empty():
    # TC1
    service = MockLabelService(return_value=[])
    # 正常系：空リストが返る
    result = list_labels(service)
    assert result == []

# TC2: ラベルが1件のみ存在する場合
def test_TC2_list_labels_one():
    # TC2
    label = SimpleNamespace(id=1, name="ラベル1")
    service = MockLabelService(return_value=[label])
    result = list_labels(service)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "ラベル1"

# TC3: 複数ラベルが存在する場合
def test_TC3_list_labels_multiple():
    # TC3
    labels = [
        SimpleNamespace(id=1, name="ラベル1"),
        SimpleNamespace(id=2, name="ラベル2"),
        SimpleNamespace(id=3, name="ラベル3"),
    ]
    service = MockLabelService(return_value=labels)
    result = list_labels(service)
    assert len(result) == 3
    assert [r.id for r in result] == [1, 2, 3]
    assert [r.name for r in result] == ["ラベル1", "ラベル2", "ラベル3"]

# TC4: 大量データ時
def test_TC4_list_labels_many():
    # TC4
    labels = [SimpleNamespace(id=i, name=f"ラベル{i}") for i in range(10000)]
    service = MockLabelService(return_value=labels)
    result = list_labels(service)
    assert len(result) == 10000
    for i in range(10000):
        assert result[i].id == i
        assert result[i].name == f"ラベル{i}"

# TC5: list_labels()が不正な型を返す（例：dict）
def test_TC5_list_labels_invalid_type():
    # TC5
    service = MockLabelService(return_value={"id": 1, "name": "ラベル1"})
    with pytest.raises(TypeError):
        list_labels(service)

# TC6: list_labels()がNoneを返す
def test_TC6_list_labels_none():
    # TC6
    service = MockLabelService(return_value=None)
    with pytest.raises(TypeError):
        list_labels(service)

# TC7: list_labels()が例外を投げる
def test_TC7_list_labels_exception():
    # TC7
    service = MockLabelService(raise_exception=Exception("サービス層例外"))
    with pytest.raises(Exception):
        list_labels(service)

# TC8: ラベルの属性が不正な値を含むリストを返す（idがstr型など）
def test_TC8_list_labels_invalid_label_attribute():
    # TC8
    label = SimpleNamespace(id="不正id", name="ラベル1")  # idがstr型
    service = MockLabelService(return_value=[label])
    with pytest.raises(ValidationError):
        list_labels(service)

# TC9: ラベルの属性が欠損しているリストを返す（name欠損）
def test_TC9_list_labels_missing_attribute():
    # TC9
    label = SimpleNamespace(id=1)  # name属性なし
    service = MockLabelService(return_value=[label])
    with pytest.raises(ValidationError):
        list_labels(service)

# TC10: ラベルが存在しない場合の再現テスト（空リスト）
def test_TC10_list_labels_empty_repeat():
    # TC10
    service = MockLabelService(return_value=[])
    result = list_labels(service)
    assert result == []

# TC11: ラベルリストの一部のみ属性値が不正な場合（idがstr型のラベルを含む）
def test_TC11_list_labels_partial_invalid_attribute():
    # TC11
    valid_label = SimpleNamespace(id=1, name="ラベル1")
    invalid_label = SimpleNamespace(id="不正id", name="ラベル2")
    service = MockLabelService(return_value=[valid_label, invalid_label])
    with pytest.raises(ValidationError):
        list_labels(service)

# TC12: ラベルリストの一部のみ属性が欠損している場合（name欠損のラベルを含む）
def test_TC12_list_labels_partial_missing_attribute():
    # TC12
    valid_label = SimpleNamespace(id=1, name="ラベル1")
    missing_label = SimpleNamespace(id=2)  # name属性なし
    service = MockLabelService(return_value=[valid_label, missing_label])
    with pytest.raises(ValidationError):
        list_labels(service)

# TC13: list_labels()が空文字列を返す
def test_TC13_list_labels_empty_string():
    # TC13
    service = MockLabelService(return_value="")
    with pytest.raises(TypeError):
        list_labels(service)

# TC14: list_labels()が整数値を返す
def test_TC14_list_labels_integer():
    # TC14
    service = MockLabelService(return_value=123)
    with pytest.raises(TypeError):
        list_labels(service)

# TC15: ラベル属性値が空文字列の場合
def test_TC15_list_labels_empty_label_name():
    # TC15
    label = SimpleNamespace(id=1, name="")
    service = MockLabelService(return_value=[label])
    with pytest.raises(ValidationError):
        list_labels(service)