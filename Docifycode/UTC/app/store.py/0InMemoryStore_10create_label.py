import pytest

# テスト用のLabelクラスのダミー定義
class Label:
    def __init__(self, id, name, slug):
        self.id = id
        self.name = name
        self.slug = slug

# InMemoryStoreのテスト用インスタンス生成ヘルパー
def make_store():
    store = InMemoryStore.__new__(InMemoryStore)
    store._next_label_id = 1
    store.labels = {}
    return store

# --- TC1: 正常系: 一般的な文字列のname, slugで作成 ---
def test_create_label_tc1():
    # TC1
    store = make_store()
    label = store.create_label("test_label", "test_slug")
    assert label.name == "test_label"
    assert label.slug == "test_slug"
    assert label.id == 1

# --- TC2: 境界値: nameが空文字列 ---
def test_create_label_tc2():
    # TC2
    store = make_store()
    label = store.create_label("", "slug")
    assert label.name == ""
    assert label.slug == "slug"
    assert label.id == 1

# --- TC3: 境界値: nameが1文字 ---
def test_create_label_tc3():
    # TC3
    store = make_store()
    label = store.create_label("a", "slug")
    assert label.name == "a"
    assert label.slug == "slug"
    assert label.id == 1

# --- TC4: 境界値: nameが255文字 ---
def test_create_label_tc4():
    # TC4
    store = make_store()
    name = "a" * 255
    label = store.create_label(name, "slug")
    assert label.name == name
    assert label.slug == "slug"
    assert label.id == 1

# --- TC5: 異常系: nameがNone ---
def test_create_label_tc5():
    # TC5
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label(None, "slug")

# --- TC6: 異常系: nameがint型 ---
def test_create_label_tc6():
    # TC6
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label(123, "slug")

# --- TC7: 異常系: nameがlist型 ---
def test_create_label_tc7():
    # TC7
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label([], "slug")

# --- TC8: 異常系: nameがdict型 ---
def test_create_label_tc8():
    # TC8
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label({}, "slug")

# --- TC9: 正常系: nameが日本語 ---
def test_create_label_tc9():
    # TC9
    store = make_store()
    label = store.create_label("テスト", "slug")
    assert label.name == "テスト"
    assert label.slug == "slug"
    assert label.id == 1

# --- TC10: 正常系: nameが特殊文字を含む ---
def test_create_label_tc10():
    # TC10
    store = make_store()
    label = store.create_label("label_with_special_chars!@#", "slug")
    assert label.name == "label_with_special_chars!@#"
    assert label.slug == "slug"
    assert label.id == 1

# --- TC11: 境界値: slugが空文字列 ---
def test_create_label_tc11():
    # TC11
    store = make_store()
    label = store.create_label("test_label", "")
    assert label.name == "test_label"
    assert label.slug == ""
    assert label.id == 1

# --- TC12: 境界値: slugが1文字 ---
def test_create_label_tc12():
    # TC12
    store = make_store()
    label = store.create_label("test_label", "a")
    assert label.name == "test_label"
    assert label.slug == "a"
    assert label.id == 1

# --- TC13: 境界値: slugが255文字 ---
def test_create_label_tc13():
    # TC13
    store = make_store()
    slug = "a" * 255
    label = store.create_label("test_label", slug)
    assert label.name == "test_label"
    assert label.slug == slug
    assert label.id == 1

# --- TC14: 異常系: slugがNone ---
def test_create_label_tc14():
    # TC14
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label("test_label", None)

# --- TC15: 異常系: slugがint型 ---
def test_create_label_tc15():
    # TC15
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label("test_label", 123)

# --- TC16: 異常系: slugがlist型 ---
def test_create_label_tc16():
    # TC16
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label("test_label", [])

# --- TC17: 異常系: slugがdict型 ---
def test_create_label_tc17():
    # TC17
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label("test_label", {})

# --- TC18: 正常系: slugが日本語 ---
def test_create_label_tc18():
    # TC18
    store = make_store()
    label = store.create_label("test_label", "テスト")
    assert label.name == "test_label"
    assert label.slug == "テスト"
    assert label.id == 1

# --- TC19: 正常系: slugが特殊文字を含む ---
def test_create_label_tc19():
    # TC19
    store = make_store()
    label = store.create_label("test_label", "slug_with_special_chars!@#")
    assert label.name == "test_label"
    assert label.slug == "slug_with_special_chars!@#"
    assert label.id == 1

# --- TC20: 境界値: nameとslugが両方空文字列 ---
def test_create_label_tc20():
    # TC20
    store = make_store()
    label = store.create_label("", "")
    assert label.name == ""
    assert label.slug == ""
    assert label.id == 1

# --- TC21: 境界値: nameとslugが両方1文字 ---
def test_create_label_tc21():
    # TC21
    store = make_store()
    label = store.create_label("a", "a")
    assert label.name == "a"
    assert label.slug == "a"
    assert label.id == 1

# --- TC22: 境界値: nameとslugが両方255文字 ---
def test_create_label_tc22():
    # TC22
    store = make_store()
    name = "a" * 255
    slug = "a" * 255
    label = store.create_label(name, slug)
    assert label.name == name
    assert label.slug == slug
    assert label.id == 1

# --- TC23: 異常系: nameとslugが両方None ---
def test_create_label_tc23():
    # TC23
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label(None, None)

# --- TC24: 異常系: nameとslugが両方int型 ---
def test_create_label_tc24():
    # TC24
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label(123, 123)

# --- TC25: 異常系: nameとslugが両方list型 ---
def test_create_label_tc25():
    # TC25
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label([], [])

# --- TC26: 異常系: nameとslugが両方dict型 ---
def test_create_label_tc26():
    # TC26
    store = make_store()
    with pytest.raises(TypeError):
        store.create_label({}, {})

# --- TC27: 正常系: nameとslugが両方日本語 ---
def test_create_label_tc27():
    # TC27
    store = make_store()
    label = store.create_label("テスト", "テスト")
    assert label.name == "テスト"
    assert label.slug == "テスト"
    assert label.id == 1

# --- TC28: 正常系: nameとslugが両方特殊文字を含む ---
def test_create_label_tc28():
    # TC28
    store = make_store()
    label = store.create_label("label_with_special_chars!@#", "slug_with_special_chars!@#")
    assert label.name == "label_with_special_chars!@#"
    assert label.slug == "slug_with_special_chars!@#"
    assert label.id == 1
```
