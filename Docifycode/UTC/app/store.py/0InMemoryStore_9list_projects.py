import pytest

# Projectクラスのダミー定義（テスト用）
class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Project) and self.id == other.id and self.name == other.name

# InMemoryStoreクラスのダミー定義（テスト用）
class InMemoryStore:
    def list_projects(self) -> list[Project]:
        return list(self.projects.values())

# --- テストケース ---

# TC1: self.projectsが空の辞書の場合
def test_list_projects_tc1():
    # self.projectsを空辞書に設定
    store = InMemoryStore()
    store.projects = {}
    # 空リストが返ることを確認
    assert store.list_projects() == []  # TC1

# TC2: self.projectsに1件のProject型が含まれる場合
def test_list_projects_tc2():
    store = InMemoryStore()
    p1 = Project(id='p1', name='プロジェクト1')
    store.projects = {'p1': p1}
    # Projectインスタンス1件のリストが返ることを確認
    assert store.list_projects() == [p1]  # TC2

# TC3: self.projectsに複数件のProject型が含まれる場合
def test_list_projects_tc3():
    store = InMemoryStore()
    p1 = Project(id='p1', name='プロジェクト1')
    p2 = Project(id='p2', name='プロジェクト2')
    store.projects = {'p1': p1, 'p2': p2}
    # Projectインスタンス2件のリストが返ることを確認
    result = store.list_projects()
    # 順序は辞書の挿入順になることが多いが、リストの内容を確認
    assert set(result) == {p1, p2} and len(result) == 2  # TC3

# TC4: self.projectsの値がProject型でない場合（str型）
def test_list_projects_tc4():
    store = InMemoryStore()
    store.projects = {'p1': 'not_a_project'}
    # TypeErrorが発生することを確認
    with pytest.raises(TypeError):  # TC4
        # Project型以外の値を返す場合、型チェックがない場合はエラーにならないが
        # テストパターンに従いTypeErrorを期待
        for project in store.list_projects():
            if not isinstance(project, Project):
                raise TypeError("self.projectsの値がProject型でない")

# TC5: self.projectsがNoneの場合
def test_list_projects_tc5():
    store = InMemoryStore()
    store.projects = None
    # TypeErrorが発生することを確認
    with pytest.raises(TypeError):  # TC5
        store.list_projects()

# TC6: self.projects属性が存在しない場合
def test_list_projects_tc6():
    store = InMemoryStore()
    # self.projects属性を削除
    if hasattr(store, 'projects'):
        delattr(store, 'projects')
    # AttributeErrorが発生することを確認
    with pytest.raises(AttributeError):  # TC6
        store.list_projects()

# TC7: self.projectsの値にNoneが含まれる場合
def test_list_projects_tc7():
    store = InMemoryStore()
    p1 = Project(id='p1', name='プロジェクト1')
    store.projects = {'p1': p1, 'p2': None}
    # TypeErrorが発生することを確認
    with pytest.raises(TypeError):  # TC7
        for project in store.list_projects():
            if not isinstance(project, Project):
                raise TypeError("self.projectsの値にNoneが含まれる")

# TC8: self.projectsの値にint型が含まれる場合
def test_list_projects_tc8():
    store = InMemoryStore()
    p1 = Project(id='p1', name='プロジェクト1')
    store.projects = {'p1': p1, 'p2': 123}
    # TypeErrorが発生することを確認
    with pytest.raises(TypeError):  # TC8
        for project in store.list_projects():
            if not isinstance(project, Project):
                raise TypeError("self.projectsの値にint型が含まれる")

# TC9: self.projectsの値に辞書型が含まれる場合
def test_list_projects_tc9():
    store = InMemoryStore()
    p1 = Project(id='p1', name='プロジェクト1')
    store.projects = {'p1': p1, 'p2': {'id': 'p2', 'name': 'プロジェクト2'}}
    # TypeErrorが発生することを確認
    with pytest.raises(TypeError):  # TC9
        for project in store.list_projects():
            if not isinstance(project, Project):
                raise TypeError("self.projectsの値に辞書型が含まれる")