import pytest

# Projectクラスのダミー定義
class Project:
    def __init__(self, id, archived):
        self.id = id
        self.archived = archived

    def __eq__(self, other):
        return isinstance(other, Project) and self.id == other.id and self.archived == other.archived

    def __repr__(self):
        return f"Project(id={self.id}, archived={self.archived})"

# ProjectServiceのテスト用サブクラス
class DummyStore:
    def __init__(self, projects):
        self._projects = projects

    def list_projects(self):
        return self._projects

class ProjectService:
    def __init__(self, store):
        self.store = store

    def list_projects(self, archived: bool | None = None) -> list[Project]:
        # 型チェック追加（異常系テストのため）
        if archived is not None and not isinstance(archived, bool):
            raise TypeError("archived must be bool or None")
        projects = self.store.list_projects()
        if archived is not None:
            projects = [project for project in projects if project.archived is archived]
        return sorted(projects, key=lambda project: project.id)

# --- テストケース ---

# TC1: archived=None, プロジェクト2件（True/False混在）, 全件返却
def test_TC1():
    # TC1
    projects = [Project(1, True), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(None)
    assert result == sorted(projects, key=lambda p: p.id)

# TC2: archived=True, プロジェクト2件（True/False混在）, Trueのみ返却
def test_TC2():
    # TC2
    projects = [Project(1, True), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == [Project(1, True)]

# TC3: archived=False, プロジェクト2件（True/False混在）, Falseのみ返却
def test_TC3():
    # TC3
    projects = [Project(1, True), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == [Project(2, False)]

# TC4: archived=None, 空リスト, 空リスト返却
def test_TC4():
    # TC4
    projects = []
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(None)
    assert result == []

# TC5: archived=True, 空リスト, 空リスト返却
def test_TC5():
    # TC5
    projects = []
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == []

# TC6: archived=False, 空リスト, 空リスト返却
def test_TC6():
    # TC6
    projects = []
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == []

# TC7: archived=None, 全件archived=True, 全件返却
def test_TC7():
    # TC7
    projects = [Project(1, True), Project(2, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(None)
    assert result == sorted(projects, key=lambda p: p.id)

# TC8: archived=True, 全件archived=True, 全件返却
def test_TC8():
    # TC8
    projects = [Project(1, True), Project(2, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == sorted(projects, key=lambda p: p.id)

# TC9: archived=False, 全件archived=True, 空リスト返却
def test_TC9():
    # TC9
    projects = [Project(1, True), Project(2, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == []

# TC10: archived=None, 全件archived=False, 全件返却
def test_TC10():
    # TC10
    projects = [Project(1, False), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(None)
    assert result == sorted(projects, key=lambda p: p.id)

# TC11: archived=True, 全件archived=False, 空リスト返却
def test_TC11():
    # TC11
    projects = [Project(1, False), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == []

# TC12: archived=False, 全件archived=False, 全件返却
def test_TC12():
    # TC12
    projects = [Project(1, False), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == sorted(projects, key=lambda p: p.id)

# TC13: archived=1（int型）, TypeError発生
def test_TC13():
    # TC13
    projects = [Project(1, True), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    with pytest.raises(TypeError):
        service.list_projects(1)

# TC14: archived="string"（str型）, TypeError発生
def test_TC14():
    # TC14
    projects = [Project(1, True), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    with pytest.raises(TypeError):
        service.list_projects("string")

# TC15: archived=0.5（float型）, TypeError発生
def test_TC15():
    # TC15
    projects = [Project(1, True), Project(2, False)]
    service = ProjectService(DummyStore(projects))
    with pytest.raises(TypeError):
        service.list_projects(0.5)

# TC16: archived=True, True/False混在, Trueのみ複数返却
def test_TC16():
    # TC16
    projects = [Project(1, True), Project(2, False), Project(3, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == [Project(1, True), Project(3, True)]

# TC17: archived=False, True/False混在, Falseのみ複数返却
def test_TC17():
    # TC17
    projects = [Project(1, True), Project(2, False), Project(3, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == [Project(2, False), Project(3, False)]

# TC18: archived=None, プロジェクト1件のみ, 1件返却
def test_TC18():
    # TC18
    projects = [Project(1, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(None)
    assert result == [Project(1, True)]

# TC19: archived=True, プロジェクト1件のみarchived=True, 1件返却
def test_TC19():
    # TC19
    projects = [Project(1, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == [Project(1, True)]

# TC20: archived=False, プロジェクト1件のみarchived=True, 空リスト返却
def test_TC20():
    # TC20
    projects = [Project(1, True)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == []

# TC21: archived=True, プロジェクト1件のみarchived=False, 空リスト返却
def test_TC21():
    # TC21
    projects = [Project(1, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(True)
    assert result == []

# TC22: archived=False, プロジェクト1件のみarchived=False, 1件返却
def test_TC22():
    # TC22
    projects = [Project(1, False)]
    service = ProjectService(DummyStore(projects))
    result = service.list_projects(False)
    assert result == [Project(1, False)]