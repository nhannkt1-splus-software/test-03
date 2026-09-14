import pytest

# --- テスト用ダミークラス・定数定義 ---
# OPENISH_STATUSESのダミー定義
OPENISH_STATUSES = {"open", "in_progress"}

# Ticketダミークラス
class Ticket:
    def __init__(self, project_id, status):
        self.project_id = project_id
        self.status = status

# Projectダミークラス
class Project:
    def __init__(self, id, archived=False):
        self.id = id
        self.archived = archived

# storeダミークラス
class DummyStore:
    def __init__(self, tickets):
        self._tickets = tickets

    def list_all(self):
        return self._tickets

# ProjectArchivedErrorダミー
class ProjectArchivedError(Exception):
    def __init__(self, project_id, action):
        self.project_id = project_id
        self.action = action

# ProjectHasOpenTicketsErrorダミー
class ProjectHasOpenTicketsError(Exception):
    def __init__(self, project_id, open_count):
        self.project_id = project_id
        self.open_count = open_count

# ProjectNotFoundErrorダミー
class ProjectNotFoundError(Exception):
    def __init__(self, project_id):
        self.project_id = project_id

# --- テスト対象クラスのダミー実装 ---
from types import MethodType

class ProjectService:
    def __init__(self, store, projects):
        self.store = store
        self._projects = projects

    # get_projectをテスト用にモック
    def get_project(self, project_id):
        # 型チェック
        if not isinstance(project_id, int):
            raise TypeError("project_id must be int")
        if project_id <= 0:
            raise ProjectNotFoundError(project_id)
        for p in self._projects:
            if p.id == project_id:
                return p
        raise ProjectNotFoundError(project_id)

    # archiveは元コードそのまま
    def archive(self, project_id: int) -> Project:
        project = self.get_project(project_id)
        if project.archived:
            raise ProjectArchivedError(project_id, "archive")
        open_count = sum(
            1
            for ticket in self.store.list_all()
            if ticket.project_id == project.id and ticket.status in OPENISH_STATUSES
        )
        if open_count:
            raise ProjectHasOpenTicketsError(project.id, open_count)
        project.archived = True
        return project

# --- テストケース ---
# TC1: 正常系：未アーカイブかつチケットなし
def test_archive_tc1():
    # TC1
    # プロジェクト未アーカイブ、チケットなし
    project = Project(id=1, archived=False)
    store = DummyStore([])
    service = ProjectService(store, [project])
    # 実行
    result = service.archive(1)
    # archivedがTrueになっていることを確認
    assert result.archived is True
    assert result.id == 1

# TC2: 異常系：未アーカイブだが未完了チケットあり
def test_archive_tc2():
    # TC2
    project = Project(id=1, archived=False)
    tickets = [
        Ticket(project_id=1, status="open"),
        Ticket(project_id=1, status="closed"),
    ]
    store = DummyStore(tickets)
    service = ProjectService(store, [project])
    with pytest.raises(ProjectHasOpenTicketsError) as e:
        service.archive(1)
    assert e.value.project_id == 1
    assert e.value.open_count == 1

# TC3: 異常系：既にアーカイブ済み
def test_archive_tc3():
    # TC3
    project = Project(id=1, archived=True)
    store = DummyStore([])
    service = ProjectService(store, [project])
    with pytest.raises(ProjectArchivedError) as e:
        service.archive(1)
    assert e.value.project_id == 1
    assert e.value.action == "archive"

# TC4: 異常系：存在しないproject_id
def test_archive_tc4():
    # TC4
    project = Project(id=1, archived=False)
    store = DummyStore([])
    service = ProjectService(store, [project])
    with pytest.raises(ProjectNotFoundError) as e:
        service.archive(9999)
    assert e.value.project_id == 9999

# TC5: 異常系：project_idが0（存在しない場合）
def test_archive_tc5():
    # TC5
    project = Project(id=1, archived=False)
    store = DummyStore([])
    service = ProjectService(store, [project])
    with pytest.raises(ProjectNotFoundError) as e:
        service.archive(0)
    assert e.value.project_id == 0

# TC6: 異常系：project_idが負の値（存在しない場合）
def test_archive_tc6():
    # TC6
    project = Project(id=1, archived=False)
    store = DummyStore([])
    service = ProjectService(store, [project])
    with pytest.raises(ProjectNotFoundError) as e:
        service.archive(-1)
    assert e.value.project_id == -1

# TC7: 異常系：project_idが文字列型
def test_archive_tc7():
    # TC7
    project = Project(id=1, archived=False)
    store = DummyStore([])
    service = ProjectService(store, [project])
    with pytest.raises(TypeError):
        service.archive("abc")

# TC8: 異常系：project_idがNone
def test_archive_tc8():
    # TC8
    project = Project(id=1, archived=False)
    store = DummyStore([])
    service = ProjectService(store, [project])
    with pytest.raises(TypeError):
        service.archive(None)

# TC9: 異常系：store.list_all()の戻り値型不一致
def test_archive_tc9():
    # TC9
    project = Project(id=1, archived=False)
    # store.list_all()がintを返すようにする
    class BadStore:
        def list_all(self):
            return 123  # 型不一致
    store = BadStore()
    service = ProjectService(store, [project])
    with pytest.raises(TypeError):
        service.archive(1)

# TC10: 正常系：未アーカイブかつ全て完了済みチケットのみ
def test_archive_tc10():
    # TC10
    project = Project(id=1, archived=False)
    tickets = [
        Ticket(project_id=1, status="closed"),
        Ticket(project_id=1, status="resolved"),
    ]
    store = DummyStore(tickets)
    service = ProjectService(store, [project])
    result = service.archive(1)
    assert result.archived is True
    assert result.id == 1

# TC11: 異常系：未アーカイブだが未完了チケットが複数件
def test_archive_tc11():
    # TC11
    project = Project(id=1, archived=False)
    tickets = [
        Ticket(project_id=1, status="open"),
        Ticket(project_id=1, status="in_progress"),
        Ticket(project_id=1, status="closed"),
    ]
    store = DummyStore(tickets)
    service = ProjectService(store, [project])
    with pytest.raises(ProjectHasOpenTicketsError) as e:
        service.archive(1)
    assert e.value.project_id == 1
    assert e.value.open_count == 2

# TC12: 異常系：既にアーカイブ済みかつ未完了チケットあり
def test_archive_tc12():
    # TC12
    project = Project(id=1, archived=True)
    tickets = [
        Ticket(project_id=1, status="open"),
        Ticket(project_id=1, status="closed"),
    ]
    store = DummyStore(tickets)
    service = ProjectService(store, [project])
    with pytest.raises(ProjectArchivedError) as e:
        service.archive(1)
    assert e.value.project_id == 1
    assert e.value.action == "archive"