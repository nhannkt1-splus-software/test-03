import pytest

# テスト対象のクラスとProjectクラスのダミー定義
class Project:
    def __init__(self, id, name, slug):
        self.id = id
        self.name = name
        self.slug = slug

class InMemoryStore:
    def __init__(self):
        self._next_project_id = 1
        self.projects = {}

    def create_project(self, name: str, slug: str) -> Project:
        project = Project(id=self._next_project_id, name=name, slug=slug)
        self.projects[project.id] = project
        self._next_project_id += 1
        return project

# --- 正常系テスト ---
def test_create_project_TC1():
    # TC1: 通常のプロジェクト名とスラッグ
    store = InMemoryStore()
    project = store.create_project("project1", "slug1")
    # プロジェクト名とスラッグが正しく設定されているか確認
    assert project.name == "project1"  # TC1
    assert project.slug == "slug1"     # TC1
    assert project.id == 1             # TC1

def test_create_project_TC2():
    # TC2: 日本語やハイフンを含む入力
    store = InMemoryStore()
    project = store.create_project("プロジェクト名_日本語", "slug-with-hyphens")
    assert project.name == "プロジェクト名_日本語"  # TC2
    assert project.slug == "slug-with-hyphens"     # TC2
    assert project.id == 1                         # TC2

def test_create_project_TC3():
    # TC3: プロジェクト名が空文字列
    store = InMemoryStore()
    project = store.create_project("", "slug1")
    assert project.name == ""      # TC3
    assert project.slug == "slug1" # TC3
    assert project.id == 1         # TC3

def test_create_project_TC4():
    # TC4: スラッグが空文字列
    store = InMemoryStore()
    project = store.create_project("project1", "")
    assert project.name == "project1" # TC4
    assert project.slug == ""         # TC4
    assert project.id == 1            # TC4

def test_create_project_TC5():
    # TC5: プロジェクト名が255文字
    store = InMemoryStore()
    name = "a" * 255
    project = store.create_project(name, "slug1")
    assert project.name == name       # TC5
    assert project.slug == "slug1"    # TC5
    assert project.id == 1            # TC5

def test_create_project_TC6():
    # TC6: スラッグが255文字
    store = InMemoryStore()
    slug = "a" * 255
    project = store.create_project("project1", slug)
    assert project.name == "project1" # TC6
    assert project.slug == slug       # TC6
    assert project.id == 1            # TC6

def test_create_project_TC13():
    # TC13: プロジェクト名とスラッグが両方とも空文字列
    store = InMemoryStore()
    project = store.create_project("", "")
    assert project.name == ""         # TC13
    assert project.slug == ""         # TC13
    assert project.id == 1            # TC13

def test_create_project_TC14():
    # TC14: プロジェクト名とスラッグが両方とも255文字
    store = InMemoryStore()
    name = "a" * 255
    slug = "a" * 255
    project = store.create_project(name, slug)
    assert project.name == name       # TC14
    assert project.slug == slug       # TC14
    assert project.id == 1            # TC14

# --- 異常系テスト ---
@pytest.mark.parametrize("name, slug, tcid", [
    (None, "slug1", "TC7"),      # nameがNone型
    (123, "slug1", "TC8"),       # nameがint型
    ([], "slug1", "TC9"),        # nameがlist型
])
def test_create_project_invalid_name(name, slug, tcid):
    # 異常系: nameが不正な型の場合
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_project(name, slug)  # tcid

@pytest.mark.parametrize("name, slug, tcid", [
    ("project1", None, "TC10"),      # slugがNone型
    ("project1", 123, "TC11"),       # slugがint型
    ("project1", [], "TC12"),        # slugがlist型
])
def test_create_project_invalid_slug(name, slug, tcid):
    # 異常系: slugが不正な型の場合
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_project(name, slug)  # tcid

@pytest.mark.parametrize("name, slug, tcid", [
    (None, None, "TC15"),      # nameとslugが両方ともNone型
    (123, 123, "TC16"),        # nameとslugが両方ともint型
    ([], [], "TC17"),          # nameとslugが両方ともlist型
])
def test_create_project_invalid_both(name, slug, tcid):
    # 異常系: nameとslugが両方とも不正な型の場合
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_project(name, slug)  # tcid
```
