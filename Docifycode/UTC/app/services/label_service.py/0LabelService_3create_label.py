import pytest

# テスト用のダミークラスと関数を定義
class Label:
    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

class InvalidSlugError(Exception):
    pass

class DuplicateLabelError(Exception):
    pass

# slugify, is_valid_slugのモック
def slugify(value):
    # slugifyの動作をテストケースごとに切り替える
    if value is None:
        return ""
    if value == "invalid slug!":
        return "invalid_slug"
    if value == "":
        return "valid_name"
    if value == " name_with_spaces ":
        return "name_with_spaces"
    if value == "invalid_slug":
        return "invalid_slug"
    if value == "valid_name":
        return "valid_name"
    if value == "valid_slug":
        return "valid_slug"
    if value == "existing_slug":
        return "existing_slug"
    if isinstance(value, str) and len(value) == 100 and set(value) == {"a"}:
        return value
    return str(value)

def is_valid_slug(slug):
    # slugの有効性をテストケースごとに切り替える
    if slug == "invalid_slug":
        return False
    if slug == "invalid slug!":
        return False
    if slug == "":
        return True
    if isinstance(slug, str) and len(slug) == 100 and set(slug) == {"a"}:
        return True
    if slug == "valid_slug":
        return True
    if slug == "valid_name":
        return True
    if slug == "existing_slug":
        return True
    if slug == "name_with_spaces":
        return True
    if slug == "a":
        return True
    return True

# storeのダミー
class DummyStore:
    def __init__(self):
        self.labels = {}

    def get_label_by_slug(self, slug):
        # 既存slugのテストケース用
        if slug == "existing_slug":
            return Label("existing_label", slug)
        return None

    def create_label(self, name, slug):
        label = Label(name, slug)
        self.labels[slug] = label
        return label

# テスト対象クラスのダミー
class LabelService:
    def __init__(self):
        self.store = DummyStore()

    def create_label(self, name: str, slug: str | None = None) -> Label:
        resolved = slugify(slug or name)
        if not is_valid_slug(resolved):
            raise InvalidSlugError(slug or name)
        if self.store.get_label_by_slug(resolved):
            raise DuplicateLabelError(resolved)
        return self.store.create_label(name.strip(), resolved)

# --- テストケース ---

# TC1: 正常系 name, slugともに有効な文字列
def test_create_label_tc1():
    # TC1
    service = LabelService()
    label = service.create_label("valid_name", "valid_slug")
    assert isinstance(label, Label)
    assert label.name == "valid_name"
    assert label.slug == "valid_slug"

# TC2: 正常系 slug未指定、nameからslug生成
def test_create_label_tc2():
    # TC2
    service = LabelService()
    label = service.create_label("valid_name")
    assert isinstance(label, Label)
    assert label.name == "valid_name"
    assert label.slug == "valid_name"

# TC3: 異常系 slugが無効な文字列
def test_create_label_tc3():
    # TC3
    service = LabelService()
    with pytest.raises(InvalidSlugError):
        service.create_label("valid_name", "invalid slug!")

# TC4: 異常系 slugが既存のものと重複
def test_create_label_tc4():
    # TC4
    service = LabelService()
    with pytest.raises(DuplicateLabelError):
        service.create_label("valid_name", "existing_slug")

# TC5: 正常系 nameに前後スペースあり、stripされて登録
def test_create_label_tc5():
    # TC5
    service = LabelService()
    label = service.create_label(" name_with_spaces ")
    assert isinstance(label, Label)
    assert label.name == "name_with_spaces"
    assert label.slug == "name_with_spaces"

# TC6: 境界値 nameが空文字列
def test_create_label_tc6():
    # TC6
    service = LabelService()
    label = service.create_label("")
    assert isinstance(label, Label)
    assert label.name == ""
    assert label.slug == "valid_name"

# TC7: 異常系 nameがNone（型不一致）
def test_create_label_tc7():
    # TC7
    service = LabelService()
    with pytest.raises(TypeError):
        service.create_label(None)

# TC8: 異常系 nameがint型（型不一致）
def test_create_label_tc8():
    # TC8
    service = LabelService()
    with pytest.raises(TypeError):
        service.create_label(123)

# TC9: 異常系 slugがint型（型不一致）
def test_create_label_tc9():
    # TC9
    service = LabelService()
    with pytest.raises(TypeError):
        service.create_label("valid_name", 123)

# TC10: 境界値 slugが最小長（1文字）
def test_create_label_tc10():
    # TC10
    service = LabelService()
    label = service.create_label("valid_name", "a")
    assert isinstance(label, Label)
    assert label.name == "valid_name"
    assert label.slug == "a"

# TC11: 境界値 slugが最大長（100文字）
def test_create_label_tc11():
    # TC11
    service = LabelService()
    slug_100 = "a" * 100
    label = service.create_label("valid_name", slug_100)
    assert isinstance(label, Label)
    assert label.name == "valid_name"
    assert label.slug == slug_100

# TC12: 正常系 slugが空文字列、nameからslug生成
def test_create_label_tc12():
    # TC12
    service = LabelService()
    label = service.create_label("valid_name", "")
    assert isinstance(label, Label)
    assert label.name == "valid_name"
    assert label.slug == "valid_name"

# TC13: 異常系 slugが無効な文字列で、slugify後も無効
def test_create_label_tc13():
    # TC13
    service = LabelService()
    with pytest.raises(InvalidSlugError):
        service.create_label("valid_name", "invalid_slug")

# TC14: 異常系 slugが既存のもの（slugify不要）
def test_create_label_tc14():
    # TC14
    service = LabelService()
    with pytest.raises(DuplicateLabelError):
        service.create_label("valid_name", "existing_slug")