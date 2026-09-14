import pytest

# Labelクラスのダミー定義（テスト用）
class Label:
    def __init__(self, slug):
        self.slug = slug

# InMemoryStoreクラスのダミー定義（テスト用）
class InMemoryStore:
    def __init__(self):
        # テスト用ラベルデータ
        self.labels = {
            1: Label("existing_slug"),
            2: Label("a"),
            3: Label("slug-with-special_chars!@#"),
            4: Label("a" * 100),
            5: Label(""),  # 空文字slug
        }

    # テスト対象メソッド
    def get_label_by_slug(self, slug):
        for label in self.labels.values():
            if label.slug == slug:
                return label
        return None

# --- 正常系・境界値テスト ---

# TC1: 既存のslugと一致する場合
def test_get_label_by_slug_existing_slug_TC1():
    # TC1
    store = InMemoryStore()
    result = store.get_label_by_slug("existing_slug")
    # 期待値: Labelインスタンス
    assert isinstance(result, Label)
    assert result.slug == "existing_slug"

# TC2: 一致するslugが存在しない場合
def test_get_label_by_slug_non_existing_slug_TC2():
    # TC2
    store = InMemoryStore()
    result = store.get_label_by_slug("non_existing_slug")
    # 期待値: None
    assert result is None

# TC3: 空文字列slug
def test_get_label_by_slug_empty_string_TC3():
    # TC3
    store = InMemoryStore()
    result = store.get_label_by_slug("")
    # 期待値: Labelインスタンス（空文字slug）
    assert isinstance(result, Label)
    assert result.slug == ""

# TC4: 1文字slug
def test_get_label_by_slug_one_char_TC4():
    # TC4
    store = InMemoryStore()
    result = store.get_label_by_slug("a")
    # 期待値: Labelインスタンス（slug="a"）
    assert isinstance(result, Label)
    assert result.slug == "a"

# TC5: 特殊文字を含むslug
def test_get_label_by_slug_special_chars_TC5():
    # TC5
    store = InMemoryStore()
    result = store.get_label_by_slug("slug-with-special_chars!@#")
    # 期待値: Labelインスタンス（特殊文字slug）
    assert isinstance(result, Label)
    assert result.slug == "slug-with-special_chars!@#"

# TC6: 100文字の長いslug
def test_get_label_by_slug_long_slug_TC6():
    # TC6
    store = InMemoryStore()
    long_slug = "a" * 100
    result = store.get_label_by_slug(long_slug)
    # 期待値: Labelインスタンス（長いslug）
    assert isinstance(result, Label)
    assert result.slug == long_slug

# --- 異常系テスト ---

# TC7: slugにNoneを指定した場合
def test_get_label_by_slug_none_TC7():
    # TC7
    store = InMemoryStore()
    with pytest.raises(AttributeError):
        store.get_label_by_slug(None)

# TC8: slugにint型を指定した場合
def test_get_label_by_slug_int_TC8():
    # TC8
    store = InMemoryStore()
    with pytest.raises(AttributeError):
        store.get_label_by_slug(123)

# TC9: slugにlist型を指定した場合
def test_get_label_by_slug_list_TC9():
    # TC9
    store = InMemoryStore()
    with pytest.raises(AttributeError):
        store.get_label_by_slug([])

# TC10: slugにdict型を指定した場合
def test_get_label_by_slug_dict_TC10():
    # TC10
    store = InMemoryStore()
    with pytest.raises(AttributeError):
        store.get_label_by_slug({})

# --- 部分適用テスト ---
# Pythonでは部分適用はfunctools.partialで実現可能

from functools import partial

# TC11: 部分適用 - 既存のslug
def test_partial_get_label_by_slug_existing_slug_TC11():
    # TC11
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, "existing_slug")
    result = partial_func()
    assert isinstance(result, Label)
    assert result.slug == "existing_slug"

# TC12: 部分適用 - 存在しないslug
def test_partial_get_label_by_slug_non_existing_slug_TC12():
    # TC12
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, "non_existing_slug")
    result = partial_func()
    assert result is None

# TC13: 部分適用 - 空文字列
def test_partial_get_label_by_slug_empty_string_TC13():
    # TC13
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, "")
    result = partial_func()
    assert isinstance(result, Label)
    assert result.slug == ""

# TC14: 部分適用 - 1文字slug
def test_partial_get_label_by_slug_one_char_TC14():
    # TC14
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, "a")
    result = partial_func()
    assert isinstance(result, Label)
    assert result.slug == "a"

# TC15: 部分適用 - 特殊文字slug
def test_partial_get_label_by_slug_special_chars_TC15():
    # TC15
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, "slug-with-special_chars!@#")
    result = partial_func()
    assert isinstance(result, Label)
    assert result.slug == "slug-with-special_chars!@#"

# TC16: 部分適用 - 100文字slug
def test_partial_get_label_by_slug_long_slug_TC16():
    # TC16
    store = InMemoryStore()
    long_slug = "a" * 100
    partial_func = partial(store.get_label_by_slug, long_slug)
    result = partial_func()
    assert isinstance(result, Label)
    assert result.slug == long_slug

# TC17: 部分適用 - None型
def test_partial_get_label_by_slug_none_TC17():
    # TC17
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, None)
    with pytest.raises(AttributeError):
        partial_func()

# TC18: 部分適用 - int型
def test_partial_get_label_by_slug_int_TC18():
    # TC18
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, 123)
    with pytest.raises(AttributeError):
        partial_func()

# TC19: 部分適用 - list型
def test_partial_get_label_by_slug_list_TC19():
    # TC19
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, [])
    with pytest.raises(AttributeError):
        partial_func()

# TC20: 部分適用 - dict型
def test_partial_get_label_by_slug_dict_TC20():
    # TC20
    store = InMemoryStore()
    partial_func = partial(store.get_label_by_slug, {})
    with pytest.raises(AttributeError):
        partial_func()