import pytest

# テスト対象の例外クラスとProject型をインポート
from target_module import ProjectService, InvalidSlugError, DuplicateProjectError, Project

# テスト用のモック関数とモックストア
class MockStore:
    def __init__(self):
        self.projects = {}

    def get_project_by_slug(self, slug):
        # スラッグが存在する場合はProjectオブジェクトを返す
        return self.projects.get(slug)

    def create_project(self, name, slug):
        # Projectオブジェクトを生成して返す
        project = Project(name, slug)
        self.projects[slug] = project
        return project

# テスト用のモックslugify関数
def mock_slugify(value):
    # 特殊文字や無効なスラッグをテストケースごとに制御
    if value is None:
        return None
    if value == "invalid slug!":
        return "invalid slug!"
    if value == "":
        return "valid_project_name"  # 空文字slugの場合はnameから生成
    if value == "プロジェクト名@特殊文字":
        return "invalid_slug"  # 特殊文字の場合は無効なスラッグ
    if value == "valid_slug":
        return "valid_slug"
    if value == "valid_project_name":
        return "valid_project_name"
    if value == "  project with spaces  ":
        return "project-with-spaces"
    return str(value)

# テスト用のモックis_valid_slug関数
def mock_is_valid_slug(slug):
    # 有効・無効なスラッグをテストケースごとに制御
    if slug in ["invalid slug!", "invalid_slug", None]:
        return False
    return True

# ProjectServiceの依存関数をパッチするfixture
@pytest.fixture
def patched_service(monkeypatch):
    service = ProjectService()
    service.store = MockStore()
    monkeypatch.setattr("target_module.slugify", mock_slugify)
    monkeypatch.setattr("target_module.is_valid_slug", mock_is_valid_slug)
    return service

# Projectオブジェクトのダミー定義
class Project:
    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

# --- テストケース ---
# TC1: slugがNone、nameから有効なスラッグ生成、プロジェクトが存在しない場合
def test_create_project_tc1(patched_service):
    # TC1
    result = patched_service.create_project("valid_project_name", None)
    assert isinstance(result, Project)
    assert result.name == "valid_project_name"
    assert result.slug == "valid_project_name"

# TC2: nameの前後に空白、stripされてプロジェクト作成
def test_create_project_tc2(patched_service):
    # TC2
    result = patched_service.create_project("  project with spaces  ", None)
    assert isinstance(result, Project)
    assert result.name == "project with spaces"
    assert result.slug == "project-with-spaces"

# TC3: nameに特殊文字、スラッグが無効
def test_create_project_tc3(patched_service):
    # TC3
    with pytest.raises(InvalidSlugError):
        patched_service.create_project("プロジェクト名@特殊文字", None)

# TC4: slugが有効、プロジェクトが存在しない場合
def test_create_project_tc4(patched_service):
    # TC4
    result = patched_service.create_project("valid_project_name", "valid_slug")
    assert isinstance(result, Project)
    assert result.name == "valid_project_name"
    assert result.slug == "valid_slug"

# TC5: slugが無効
def test_create_project_tc5(patched_service):
    # TC5
    with pytest.raises(InvalidSlugError):
        patched_service.create_project("valid_project_name", "invalid slug!")

# TC6: slugが有効、既存プロジェクトが存在する場合
def test_create_project_tc6(patched_service):
    # TC6
    # 事前にプロジェクトを追加
    patched_service.store.projects["valid_slug"] = Project("other", "valid_slug")
    with pytest.raises(DuplicateProjectError):
        patched_service.create_project("valid_project_name", "valid_slug")

# TC7: nameが空文字、スラッグが無効
def test_create_project_tc7(patched_service):
    # TC7
    with pytest.raises(InvalidSlugError):
        patched_service.create_project("", None)

# TC8: nameがNone（型不一致）
def test_create_project_tc8(patched_service):
    # TC8
    with pytest.raises(TypeError):
        patched_service.create_project(None, None)

# TC9: nameがint型（型不一致）
def test_create_project_tc9(patched_service):
    # TC9
    with pytest.raises(TypeError):
        patched_service.create_project(123, None)

# TC10: slugがint型（型不一致）
def test_create_project_tc10(patched_service):
    # TC10
    with pytest.raises(TypeError):
        patched_service.create_project("valid_project_name", 123)

# TC11: slugが空文字、nameからスラッグ生成し有効ならプロジェクト作成
def test_create_project_tc11(patched_service):
    # TC11
    result = patched_service.create_project("valid_project_name", "")
    assert isinstance(result, Project)
    assert result.name == "valid_project_name"
    assert result.slug == "valid_project_name"

# TC12: slugが空文字、nameから生成したスラッグが無効
def test_create_project_tc12(monkeypatch):
    # TC12
    service = ProjectService()
    service.store = MockStore()
    # slugifyが空文字の場合、無効なスラッグを返すようにパッチ
    monkeypatch.setattr("target_module.slugify", lambda v: "invalid_slug")
    monkeypatch.setattr("target_module.is_valid_slug", lambda s: False)
    with pytest.raises(InvalidSlugError):
        service.create_project("valid_project_name", "")

# TC13: slugがNone、nameから生成したスラッグが有効、既存プロジェクトが存在する場合
def test_create_project_tc13(patched_service):
    # TC13
    patched_service.store.projects["valid_project_name"] = Project("other", "valid_project_name")
    with pytest.raises(DuplicateProjectError):
        patched_service.create_project("valid_project_name", None)

# TC14: slugが無効、既存プロジェクトが存在する場合でもスラッグ検証でエラー
def test_create_project_tc14(patched_service):
    # TC14
    patched_service.store.projects["invalid slug!"] = Project("other", "invalid slug!")
    with pytest.raises(InvalidSlugError):
        patched_service.create_project("valid_project_name", "invalid slug!")

# TC15: nameが空文字、slugが有効ならプロジェクト作成可能
def test_create_project_tc15(patched_service):
    # TC15
    result = patched_service.create_project("", "valid_slug")
    assert isinstance(result, Project)
    assert result.name == ""
    assert result.slug == "valid_slug"

# TC16: nameが空文字、slugが有効だが既存プロジェクトが存在する場合
def test_create_project_tc16(patched_service):
    # TC16
    patched_service.store.projects["valid_slug"] = Project("other", "valid_slug")
    with pytest.raises(DuplicateProjectError):
        patched_service.create_project("", "valid_slug")

# TC17: nameが特殊文字でもslugが有効ならプロジェクト作成可能
def test_create_project_tc17(patched_service):
    # TC17
    result = patched_service.create_project("プロジェクト名@特殊文字", "valid_slug")
    assert isinstance(result, Project)
    assert result.name == "プロジェクト名@特殊文字"
    assert result.slug == "valid_slug"

# TC18: nameが特殊文字、slugが有効だが既存プロジェクトが存在する場合
def test_create_project_tc18(patched_service):
    # TC18
    patched_service.store.projects["valid_slug"] = Project("other", "valid_slug")
    with pytest.raises(DuplicateProjectError):
        patched_service.create_project("プロジェクト名@特殊文字", "valid_slug")

# TC19: slugがNone、nameから生成したスラッグが無効（既存プロジェクトが存在する場合でもスラッグ検証でエラー）
def test_create_project_tc19(monkeypatch):
    # TC19
    service = ProjectService()
    service.store = MockStore()
    # slugifyが無効なスラッグを返すようにパッチ
    monkeypatch.setattr("target_module.slugify", lambda v: "invalid_slug")
    monkeypatch.setattr("target_module.is_valid_slug", lambda s: False)
    service.store.projects["invalid_slug"] = Project("other", "invalid_slug")
    with pytest.raises(InvalidSlugError):
        service.create_project("valid_project_name", None)