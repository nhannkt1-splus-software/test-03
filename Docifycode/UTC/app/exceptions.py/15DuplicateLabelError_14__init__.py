import pytest

# テスト対象クラスのインポート
from target_module import DuplicateLabelError  # target_moduleは実際のモジュール名に置き換えてください

# DeskErrorのモック（もし必要なら）
class DeskError(Exception):
    pass

# --- 正常系 ---

# TC1: slug="label1"（通常の英数字ラベル名）
def test_TC1_duplicate_label_error_normal_string(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = "label1"
    err = DuplicateLabelError(slug)
    # slug属性が正しいか
    assert err.slug == slug
    # メッセージが正しいか
    assert str(err) == f"Label {slug} already exists"

# TC2: slug=""（空文字列）
def test_TC2_duplicate_label_error_empty_string(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = ""
    err = DuplicateLabelError(slug)
    assert err.slug == slug
    assert str(err) == "Label  already exists"

# TC3: slug="ラベル名"（日本語ラベル名）
def test_TC3_duplicate_label_error_japanese_string(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = "ラベル名"
    err = DuplicateLabelError(slug)
    assert err.slug == slug
    assert str(err) == f"Label {slug} already exists"

# TC4: slug="label_with_special_chars!@#"（特殊文字を含むラベル名）
def test_TC4_duplicate_label_error_special_chars(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = "label_with_special_chars!@#"
    err = DuplicateLabelError(slug)
    assert err.slug == slug
    assert str(err) == f"Label {slug} already exists"

# TC5: slug="a"（1文字のラベル名）
def test_TC5_duplicate_label_error_one_char(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = "a"
    err = DuplicateLabelError(slug)
    assert err.slug == slug
    assert str(err) == f"Label {slug} already exists"

# TC6: slug="a" * 100（100文字の長いラベル名）
def test_TC6_duplicate_label_error_long_string(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = "a" * 100
    err = DuplicateLabelError(slug)
    assert err.slug == slug
    assert str(err) == f"Label {slug} already exists"

# --- 異常系 ---

# TC7: slug=123（int型）
def test_TC7_duplicate_label_error_int_type(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = 123
    with pytest.raises(TypeError):
        DuplicateLabelError(slug)

# TC8: slug=None（None型）
def test_TC8_duplicate_label_error_none_type(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = None
    with pytest.raises(TypeError):
        DuplicateLabelError(slug)

# TC9: slug=[]（list型）
def test_TC9_duplicate_label_error_list_type(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = []
    with pytest.raises(TypeError):
        DuplicateLabelError(slug)

# TC10: slug={}（dict型）
def test_TC10_duplicate_label_error_dict_type(monkeypatch):
    # DeskErrorを正しく継承できるようにパッチ
    monkeypatch.setattr("target_module.DeskError", DeskError)
    slug = {}
    with pytest.raises(TypeError):
        DuplicateLabelError(slug)
```
