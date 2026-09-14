import pytest

# テスト用のダミークラスと例外を定義
class ProjectNotFound(Exception):
    def __init__(self, project_id):
        self.project_id = project_id

class ProjectArchivedError(Exception):
    def __init__(self, project_id, action):
        self.project_id = project_id
        self.action = action

class DummyProject:
    def __init__(self, project_id, archived=False):
        self.id = project_id
        self.archived = archived

class DummyStore:
    def __init__(self):
        # project_id: DummyProject
        self.projects = {}

    def get_project(self, project_id):
        return self.projects.get(project_id, None)

# TicketServiceのインスタンスを作成するヘルパー
def make_ticket_service(projects_dict):
    service = TicketService()
    service.store = DummyStore()
    service.store.projects = projects_dict
    return service

# --- TC1 ---
def test_resolve_project_id_none_returns_none():
    # TC1: project_idがNoneの場合
    service = make_ticket_service({})
    # project_idがNoneの場合、Noneが返される
    assert service._resolve_project_id(None) is None

# --- TC2 ---
def test_resolve_project_id_valid_project_returns_id():
    # TC2: project_idが存在し、プロジェクトがアーカイブされていない場合
    project_id = 1
    projects = {1: DummyProject(1, archived=False)}
    service = make_ticket_service(projects)
    # project_idが存在し、アーカイブされていない場合、project.idが返される
    assert service._resolve_project_id(project_id) == 1

# --- TC3 ---
def test_resolve_project_id_not_found_raises():
    # TC3: project_idが存在しない場合
    project_id = 999
    service = make_ticket_service({})
    # project_idが存在しない場合、ProjectNotFound例外が発生する
    with pytest.raises(ProjectNotFound) as e:
        service._resolve_project_id(project_id)
    assert e.value.project_id == project_id

# --- TC4 ---
def test_resolve_project_id_archived_raises():
    # TC4: project_idが存在し、プロジェクトがアーカイブされている場合
    project_id = 2
    projects = {2: DummyProject(2, archived=True)}
    service = make_ticket_service(projects)
    # project_idが存在し、アーカイブされている場合、ProjectArchivedError例外が発生する
    with pytest.raises(ProjectArchivedError) as e:
        service._resolve_project_id(project_id)
    assert e.value.project_id == project_id
    assert e.value.action == "attach ticket to"

# --- TC5 ---
def test_resolve_project_id_negative_not_found_raises():
    # TC5: project_idが負の値の場合
    project_id = -1
    service = make_ticket_service({})
    # project_idが負の値の場合、ProjectNotFound例外が発生する
    with pytest.raises(ProjectNotFound) as e:
        service._resolve_project_id(project_id)
    assert e.value.project_id == project_id

# --- TC6 ---
def test_resolve_project_id_zero_not_found_raises():
    # TC6: project_idが0の場合
    project_id = 0
    service = make_ticket_service({})
    # project_idが0の場合、ProjectNotFound例外が発生する
    with pytest.raises(ProjectNotFound) as e:
        service._resolve_project_id(project_id)
    assert e.value.project_id == project_id

# --- TC7 ---
def test_resolve_project_id_str_typeerror():
    # TC7: project_idが文字列型の場合
    project_id = "abc"
    service = make_ticket_service({})
    # project_idが文字列型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        service._resolve_project_id(project_id)

# --- TC8 ---
def test_resolve_project_id_float_typeerror():
    # TC8: project_idがfloat型の場合
    project_id = 1.5
    service = make_ticket_service({})
    # project_idがfloat型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        service._resolve_project_id(project_id)

# --- TC9 ---
def test_resolve_project_id_list_typeerror():
    # TC9: project_idがリスト型の場合
    project_id = []
    service = make_ticket_service({})
    # project_idがリスト型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        service._resolve_project_id(project_id)

# --- TC10 ---
def test_resolve_project_id_dict_typeerror():
    # TC10: project_idが辞書型の場合
    project_id = {}
    service = make_ticket_service({})
    # project_idが辞書型の場合、TypeError例外が発生する
    with pytest.raises(TypeError):
        service._resolve_project_id(project_id)

# --- TC11 ---
def test_resolve_project_id_large_int_not_found_raises():
    # TC11: 非常に大きい整数値のproject_id
    project_id = 1000000
    service = make_ticket_service({})
    # project_idが非常に大きい値の場合、ProjectNotFound例外が発生する
    with pytest.raises(ProjectNotFound) as e:
        service._resolve_project_id(project_id)
    assert e.value.project_id == project_id

# --- TC12 ---
def test_resolve_project_id_large_negative_not_found_raises():
    # TC12: 非常に小さい負の整数値のproject_id
    project_id = -999999
    service = make_ticket_service({})
    # project_idが非常に小さい負の値の場合、ProjectNotFound例外が発生する
    with pytest.raises(ProjectNotFound) as e:
        service._resolve_project_id(project_id)
    assert e.value.project_id == project_id