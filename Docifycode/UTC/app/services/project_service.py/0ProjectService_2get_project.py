import pytest

# テスト対象クラスの依存クラス(Project, ProjectNotFound)をモックする
class Project:
    def __init__(self, project_id):
        self.project_id = project_id

class ProjectNotFound(Exception):
    def __init__(self, project_id):
        self.project_id = project_id
        super().__init__(f"Project {project_id} not found")

# ProjectServiceのstore属性をモックするためのヘルパークラス
class MockStore:
    def __init__(self, projects):
        self.projects = projects

    def get_project(self, project_id):
        return self.projects.get(project_id, None)

# テスト対象インスタンス生成ヘルパー
def create_service_with_projects(projects_dict):
    service = ProjectService()
    service.store = MockStore(projects_dict)
    return service

# TC1: project_id=1が存在する場合（正常系）
def test_get_project_tc1():
    # TC1
    # project_id=1が存在する場合
    service = create_service_with_projects({1: Project(1)})
    project = service.get_project(1)
    assert isinstance(project, Project)
    assert project.project_id == 1

# TC2: project_id=0が存在しない場合（異常系: ProjectNotFound例外）
def test_get_project_tc2():
    # TC2
    # project_id=0が存在しない場合
    service = create_service_with_projects({})
    with pytest.raises(ProjectNotFound) as exc_info:
        service.get_project(0)
    assert exc_info.value.project_id == 0

# TC3: project_id=-1が存在しない場合（異常系: ProjectNotFound例外）
def test_get_project_tc3():
    # TC3
    # project_id=-1が存在しない場合
    service = create_service_with_projects({})
    with pytest.raises(ProjectNotFound) as exc_info:
        service.get_project(-1)
    assert exc_info.value.project_id == -1

# TC4: project_id=999999が存在しない場合（異常系: ProjectNotFound例外）
def test_get_project_tc4():
    # TC4
    # project_id=999999が存在しない場合
    service = create_service_with_projects({})
    with pytest.raises(ProjectNotFound) as exc_info:
        service.get_project(999999)
    assert exc_info.value.project_id == 999999

# TC5: project_id="1"（str型: 型不一致）（異常系: TypeError例外）
def test_get_project_tc5():
    # TC5
    # project_id="1"（str型: 型不一致）
    service = create_service_with_projects({1: Project(1)})
    with pytest.raises(TypeError):
        service.get_project("1")

# TC6: project_id=None（None型: 型不一致）（異常系: TypeError例外）
def test_get_project_tc6():
    # TC6
    # project_id=None（None型: 型不一致）
    service = create_service_with_projects({1: Project(1)})
    with pytest.raises(TypeError):
        service.get_project(None)

# TC7: project_id=1.5（float型: 型不一致）（異常系: TypeError例外）
def test_get_project_tc7():
    # TC7
    # project_id=1.5（float型: 型不一致）
    service = create_service_with_projects({1: Project(1)})
    with pytest.raises(TypeError):
        service.get_project(1.5)
```
