import pytest
from pydantic import ValidationError
from fastapi import HTTPException

# テスト対象関数と依存クラスのインポート
# 必要に応じて import パスを調整してください
from target_module import create_label, LabelCreate, LabelService, DeskError, LabelOut

# LabelServiceのモック
class MockLabelService:
    def __init__(self, error=None, return_value=None):
        self.error = error
        self.return_value = return_value

    def create_label(self, name, slug):
        if self.error:
            raise self.error
        return self.return_value or {"name": name, "slug": slug}

# DeskErrorのモック
class MockDeskError(DeskError):
    pass

# LabelOutのモック（必要なら）
class MockLabelOut(LabelOut):
    @classmethod
    def model_validate(cls, value, from_attributes=False):
        return value

# --- TC1: 正常系 name, slugともに正常な値 ---
def test_create_label_tc1():
    # TC1
    payload = LabelCreate(name="ラベル名", slug="label-slug")
    service = MockLabelService(return_value={"name": "ラベル名", "slug": "label-slug"})
    result = create_label(payload, service)
    assert result["name"] == "ラベル名"
    assert result["slug"] == "label-slug"

# --- TC2: nameが空文字列 ---
def test_create_label_tc2():
    # TC2
    payload = LabelCreate(name="", slug="label-slug")
    service = MockLabelService(error=MockDeskError("nameが空"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC3: slugが空文字列 ---
def test_create_label_tc3():
    # TC3
    payload = LabelCreate(name="ラベル名", slug="")
    service = MockLabelService(error=MockDeskError("slugが空"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC4: nameが256文字の長い文字列 ---
def test_create_label_tc4():
    # TC4
    long_name = "a" * 256
    payload = LabelCreate(name=long_name, slug="label-slug")
    service = MockLabelService(error=MockDeskError("nameが長すぎる"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC5: slugが256文字の長い文字列 ---
def test_create_label_tc5():
    # TC5
    long_slug = "a" * 256
    payload = LabelCreate(name="ラベル名", slug=long_slug)
    service = MockLabelService(error=MockDeskError("slugが長すぎる"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC6: slugに特殊文字を含む ---
def test_create_label_tc6():
    # TC6
    payload = LabelCreate(name="ラベル名", slug="label_slug!@#")
    service = MockLabelService(error=MockDeskError("slugに不正文字"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC7: nameがnull ---
def test_create_label_tc7():
    # TC7
    with pytest.raises(ValidationError):
        LabelCreate(name=None, slug="label-slug")

# --- TC8: slugがnull ---
def test_create_label_tc8():
    # TC8
    with pytest.raises(ValidationError):
        LabelCreate(name="ラベル名", slug=None)

# --- TC9: nameがint型 ---
def test_create_label_tc9():
    # TC9
    with pytest.raises(ValidationError):
        LabelCreate(name=123, slug="label-slug")

# --- TC10: slugがint型 ---
def test_create_label_tc10():
    # TC10
    with pytest.raises(ValidationError):
        LabelCreate(name="ラベル名", slug=456)

# --- TC11: nameがリスト型 ---
def test_create_label_tc11():
    # TC11
    with pytest.raises(ValidationError):
        LabelCreate(name=["ラベル名"], slug="label-slug")

# --- TC12: slugがリスト型 ---
def test_create_label_tc12():
    # TC12
    with pytest.raises(ValidationError):
        LabelCreate(name="ラベル名", slug=["label-slug"])

# --- TC13: 空の辞書（必須項目なし） ---
def test_create_label_tc13():
    # TC13
    with pytest.raises(ValidationError):
        LabelCreate(**{})

# --- TC14: slugが欠損 ---
def test_create_label_tc14():
    # TC14
    with pytest.raises(ValidationError):
        LabelCreate(name="ラベル名")

# --- TC15: nameが欠損 ---
def test_create_label_tc15():
    # TC15
    with pytest.raises(ValidationError):
        LabelCreate(slug="label-slug")

# --- TC16: nameとslug両方空 ---
def test_create_label_tc16():
    # TC16
    payload = LabelCreate(name="", slug="")
    service = MockLabelService(error=MockDeskError("nameとslug両方空"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC17: slug重複 ---
def test_create_label_tc17():
    # TC17
    payload = LabelCreate(name="ラベル名", slug="label-slug")
    service = MockLabelService(error=MockDeskError("slug重複"))
    with pytest.raises(HTTPException):
        create_label(payload, service)

# --- TC18: 属性値が境界値（例えばnameやslugが許容最大長） ---
def test_create_label_tc18():
    # TC18
    max_length = 255  # 境界値（仮定）
    payload = LabelCreate(name="a" * max_length, slug="b" * max_length)
    service = MockLabelService(return_value={"name": "a" * max_length, "slug": "b" * max_length})
    result = create_label(payload, service)
    assert result["name"] == "a" * max_length
    assert result["slug"] == "b" * max_length

# --- TC19: 属性値が正しい場合（DB重複以外の異常なし） ---
def test_create_label_tc19():
    # TC19
    payload = LabelCreate(name="ラベル名", slug="label-slug")
    service = MockLabelService(return_value={"name": "ラベル名", "slug": "label-slug"})
    result = create_label(payload, service)
    assert result["name"] == "ラベル名"
    assert result["slug"] == "label-slug"
```
