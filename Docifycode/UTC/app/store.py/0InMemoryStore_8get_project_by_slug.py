import pytest

# テスト用のダミーProjectクラスを定義
class Project:
    def __init__(self, slug):
        self.slug = slug

# テスト対象のInMemoryStoreクラスをインポート
from types import SimpleNamespace

# テスト対象メソッドを持つInMemoryStoreクラスをimportまたは定義済みと仮定

@pytest.fixture
def store_with_projects():
    # slug: "valid_slug", "slug_with_special_chars!@#", "slug_with_100_chars"
    store = InMemoryStore()
    # 100文字のslug
    long_slug = "a" * 100
    store.projects = {
        1: Project("valid_slug"),
        2: Project("slug_with_special_chars!@#"),
        3: Project(long_slug),
    }
    return store

@pytest.fixture
def store_empty():
    store = InMemoryStore()
    store.projects = {}
    return store

@pytest.fixture
def store_without_slug_attr():
    # slug属性を持たないProjectインスタンスを含む
    store = InMemoryStore()
    class NoSlug:
        pass
    store.projects = {1: NoSlug()}
    return store

# TC1: projectsにslugが一致するProjectが存在する場合
def test_get_project_by_slug_valid_slug_found(store_with_projects):
    # TC1
    result = store_with_projects.get_project_by_slug("valid_slug")
    # Projectインスタンスが返ることを確認
    assert isinstance(result, Project)
    assert result.slug == "valid_slug"

# TC2: projectsにslugが一致するProjectが存在しない場合
def test_get_project_by_slug_nonexistent_slug(store_with_projects):
    # TC2
    result = store_with_projects.get_project_by_slug("nonexistent_slug")
    assert result is None

# TC3: 空文字列を指定した場合
def test_get_project_by_slug_empty_string(store_with_projects):
    # TC3
    result = store_with_projects.get_project_by_slug("")
    assert result is None

# TC4: slugがNone型（型不一致）の場合
def test_get_project_by_slug_none_type(store_with_projects):
    # TC4
    with pytest.raises(TypeError):
        store_with_projects.get_project_by_slug(None)

# TC5: slugがint型（型不一致）の場合
def test_get_project_by_slug_int_type(store_with_projects):
    # TC5
    with pytest.raises(TypeError):
        store_with_projects.get_project_by_slug(123)

# TC6: slugがlist型（型不一致）の場合
def test_get_project_by_slug_list_type(store_with_projects):
    # TC6
    with pytest.raises(TypeError):
        store_with_projects.get_project_by_slug([])

# TC7: slugがdict型（型不一致）の場合
def test_get_project_by_slug_dict_type(store_with_projects):
    # TC7
    with pytest.raises(TypeError):
        store_with_projects.get_project_by_slug({})

# TC8: 特殊文字を含むslugで一致するProjectが存在しない場合
def test_get_project_by_slug_special_chars_not_found(store_with_projects):
    # TC8
    result = store_with_projects.get_project_by_slug("not_exist!@#")
    assert result is None

# TC9: 100文字の長いslugで一致するProjectが存在しない場合
def test_get_project_by_slug_long_slug_not_found(store_with_projects):
    # TC9
    long_slug = "b" * 100
    result = store_with_projects.get_project_by_slug(long_slug)
    assert result is None

# TC10: projectsが空の場合
def test_get_project_by_slug_projects_empty(store_empty):
    # TC10
    result = store_empty.get_project_by_slug("valid_slug")
    assert result is None

# TC11: Projectインスタンスにslug属性が存在しない場合
def test_get_project_by_slug_no_slug_attr(store_without_slug_attr):
    # TC11
    with pytest.raises(AttributeError):
        store_without_slug_attr.get_project_by_slug("valid_slug")

# TC12: 特殊文字を含むslugで一致するProjectが存在する場合
def test_get_project_by_slug_special_chars_found(store_with_projects):
    # TC12
    result = store_with_projects.get_project_by_slug("slug_with_special_chars!@#")
    assert isinstance(result, Project)
    assert result.slug == "slug_with_special_chars!@#"

# TC13: 100文字の長いslugで一致するProjectが存在する場合
def test_get_project_by_slug_long_slug_found(store_with_projects):
    # TC13
    long_slug = "a" * 100
    result = store_with_projects.get_project_by_slug(long_slug)
    assert isinstance(result, Project)
    assert result.slug == long_slug