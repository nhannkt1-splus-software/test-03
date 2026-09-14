import pytest
from fastapi import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

# テスト用のモッククラスと例外
class DeskError(Exception):
    pass

class ProjectServiceMock:
    # TC1, TC9: archive成功
    def archive(self, project_id):
        pass

    # TC2, TC3, TC4: archiveでDeskError例外発生
    def archive_raise_deskerror(self, project_id):
        raise DeskError("DeskError: archive failed")

    # TC10: archiveで予期しないException発生
    def archive_raise_exception(self, project_id):
        raise Exception("Unexpected Exception")

    # TC8: list_projectsで予期しないException発生
    def list_projects_raise_exception(self):
        raise Exception("Unexpected Exception in list_projects")

    # TC12: list_projectsでDeskError例外発生
    def list_projects_raise_deskerror(self):
        raise DeskError("DeskError: list_projects failed")

    # 通常のlist_projects
    def list_projects(self):
        return ["project1", "project2"]

class TicketServiceMock:
    # 通常のlist_tickets
    def list_tickets(self):
        return ["ticket1", "ticket2"]

    # TC7: list_ticketsで予期しないException発生
    def list_tickets_raise_exception(self):
        raise Exception("Unexpected Exception in list_tickets")

    # TC11: list_ticketsでDeskError例外発生
    def list_tickets_raise_deskerror(self):
        raise DeskError("DeskError: list_tickets failed")

# テンプレートのモック
templates = Jinja2Templates(directory=".")

# archive_project_formのテスト対象関数をimportまたは定義
# ここでは直接定義（実際はimportしてください）
def archive_project_form(
    project_id: int,
    request: Request,
    projects,
    tickets,
):
    try:
        projects.archive(project_id)
        return RedirectResponse(url="/projects", status_code=303)
    except DeskError as exc:
        return templates.TemplateResponse(
            request,
            "projects.html",
            {
                "projects": projects.list_projects(),
                "tickets": tickets.list_tickets(),
                "error": str(exc),
            },
            status_code=409,
        )

# Requestのモック
class RequestMock(Request):
    def __init__(self):
        pass

@pytest.fixture
def request_mock():
    return RequestMock()

# TC1, TC9: 正常系（archive成功）
# TC1
def test_TC1_archive_success(request_mock):
    # TC1: project_id=1, projects=正常, tickets=正常
    projects = ProjectServiceMock()
    tickets = TicketServiceMock()
    response = archive_project_form(1, request_mock, projects, tickets)
    # 正常時はRedirectResponse
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/projects"

# TC9
def test_TC9_archive_success_boundary(request_mock):
    # TC9: project_id=1, projects=正常, tickets=正常（境界値）
    projects = ProjectServiceMock()
    tickets = TicketServiceMock()
    response = archive_project_form(1, request_mock, projects, tickets)
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/projects"

# TC2: archiveでDeskError例外発生（存在しないproject_id）
def test_TC2_archive_deskerror(request_mock):
    # TC2: project_id=9999, projects=archiveでDeskError, tickets=正常
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
    projects = Projects()
    tickets = TicketServiceMock()
    response = archive_project_form(9999, request_mock, projects, tickets)
    # DeskError時はTemplateResponse
    assert hasattr(response, "status_code")
    assert response.status_code == 409
    assert response.template.name == "projects.html"
    assert "error" in response.context
    assert "DeskError" in response.context["error"]

# TC3: archiveでDeskError例外発生（負のproject_id）
def test_TC3_archive_negative_id_deskerror(request_mock):
    # TC3: project_id=-1, projects=archiveでDeskError, tickets=正常
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
    projects = Projects()
    tickets = TicketServiceMock()
    response = archive_project_form(-1, request_mock, projects, tickets)
    assert hasattr(response, "status_code")
    assert response.status_code == 409
    assert response.template.name == "projects.html"
    assert "error" in response.context
    assert "DeskError" in response.context["error"]

# TC4: archiveでDeskError例外発生（project_id=0）
def test_TC4_archive_zero_id_deskerror(request_mock):
    # TC4: project_id=0, projects=archiveでDeskError, tickets=正常
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
    projects = Projects()
    tickets = TicketServiceMock()
    response = archive_project_form(0, request_mock, projects, tickets)
    assert hasattr(response, "status_code")
    assert response.status_code == 409
    assert response.template.name == "projects.html"
    assert "error" in response.context
    assert "DeskError" in response.context["error"]

# TC5: project_idが文字列型（型不一致によるTypeError）
def test_TC5_project_id_str_typeerror(request_mock):
    # TC5: project_id="abc", projects=正常, tickets=正常
    projects = ProjectServiceMock()
    tickets = TicketServiceMock()
    with pytest.raises(TypeError):
        archive_project_form("abc", request_mock, projects, tickets)

# TC6: project_idがNone（型不一致によるTypeError）
def test_TC6_project_id_none_typeerror(request_mock):
    # TC6: project_id=None, projects=正常, tickets=正常
    projects = ProjectServiceMock()
    tickets = TicketServiceMock()
    with pytest.raises(TypeError):
        archive_project_form(None, request_mock, projects, tickets)

# TC7: tickets.list_tickets()で予期しないException発生
def test_TC7_tickets_list_tickets_exception(request_mock):
    # TC7: project_id=1, projects=archiveでDeskError, tickets=list_ticketsでException
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
    class Tickets(TicketServiceMock):
        def list_tickets(self):
            raise Exception("Unexpected Exception in list_tickets")
    projects = Projects()
    tickets = Tickets()
    with pytest.raises(Exception):
        archive_project_form(1, request_mock, projects, tickets)

# TC8: projects.list_projects()で予期しないException発生
def test_TC8_projects_list_projects_exception(request_mock):
    # TC8: project_id=1, projects=list_projectsでException, tickets=正常
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
        def list_projects(self):
            raise Exception("Unexpected Exception in list_projects")
    projects = Projects()
    tickets = TicketServiceMock()
    with pytest.raises(Exception):
        archive_project_form(1, request_mock, projects, tickets)

# TC10: archive時にDeskError以外の例外発生
def test_TC10_archive_unexpected_exception(request_mock):
    # TC10: project_id=1, projects=archiveでException, tickets=正常
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise Exception("Unexpected Exception")
    projects = Projects()
    tickets = TicketServiceMock()
    with pytest.raises(Exception):
        archive_project_form(1, request_mock, projects, tickets)

# TC11: tickets.list_tickets()でDeskError以外の例外発生
def test_TC11_tickets_list_tickets_deskerror(request_mock):
    # TC11: project_id=1, projects=archiveでDeskError, tickets=list_ticketsでDeskError
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
    class Tickets(TicketServiceMock):
        def list_tickets(self):
            raise DeskError("DeskError: list_tickets failed")
    projects = Projects()
    tickets = Tickets()
    with pytest.raises(DeskError):
        archive_project_form(1, request_mock, projects, tickets)

# TC12: projects.list_projects()でDeskError以外の例外発生
def test_TC12_projects_list_projects_deskerror(request_mock):
    # TC12: project_id=1, projects=list_projectsでDeskError, tickets=正常
    class Projects(ProjectServiceMock):
        def archive(self, project_id):
            raise DeskError("DeskError: archive failed")
        def list_projects(self):
            raise DeskError("DeskError: list_projects failed")
    projects = Projects()
    tickets = TicketServiceMock()
    with pytest.raises(DeskError):
        archive_project_form(1, request_mock, projects, tickets)

# TC13: ticketsがNone（依存注入失敗によるTypeError）
def test_TC13_tickets_none_typeerror(request_mock):
    # TC13: project_id=1, projects=正常, tickets=None
    projects = ProjectServiceMock()
    tickets = None
    with pytest.raises(TypeError):
        archive_project_form(1, request_mock, projects, tickets)

# TC14: projectsがNone（依存注入失敗によるTypeError）
def test_TC14_projects_none_typeerror(request_mock):
    # TC14: project_id=1, projects=None, tickets=正常
    projects = None
    tickets = TicketServiceMock()
    with pytest.raises(TypeError):
        archive_project_form(1, request_mock, projects, tickets)