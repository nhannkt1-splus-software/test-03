import pytest
from unittest.mock import Mock
from fastapi import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

# テスト対象関数のインポート
# from <module> import create_project_form, DeskError

# テンプレートのモック
templates = Mock(spec=Jinja2Templates)
templates.TemplateResponse = Mock()

# DeskErrorのモック定義（実際の実装に合わせてインポートすること）
class DeskError(Exception):
    pass

# Requestオブジェクトのモック
class DummyRequest(Request):
    def __init__(self):
        self.scope = {"type": "http"}

@pytest.fixture
def request():
    # Requestオブジェクトのモックを返す
    return DummyRequest()

@pytest.fixture
def project_service():
    # ProjectServiceのモックインスタンス
    svc = Mock()
    svc.create_project = Mock()
    svc.list_projects = Mock(return_value=["プロジェクトA"])
    return svc

@pytest.fixture
def ticket_service():
    # TicketServiceのモックインスタンス
    svc = Mock()
    svc.list_tickets = Mock(return_value=["チケット1"])
    return svc

# TC1: slug未入力の場合
def test_create_project_form_tc1(request, project_service, ticket_service):
    # テストID: TC1
    name = "プロジェクトA"
    slug = ""
    result = create_project_form(request, name, slug, project_service, ticket_service)
    # 正常系: RedirectResponseが返ること
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC2: slug入力ありの場合
def test_create_project_form_tc2(request, project_service, ticket_service):
    # テストID: TC2
    name = "プロジェクトA"
    slug = "project-a"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC3: 特殊文字を含むプロジェクト名
def test_create_project_form_tc3(request, project_service, ticket_service):
    # テストID: TC3
    name = "プロジェクト@2024"
    slug = "project-special"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC4: 長いプロジェクト名（100文字）
def test_create_project_form_tc4(request, project_service, ticket_service):
    # テストID: TC4
    name = "a" * 100
    slug = "long-slug"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC5: nameが空文字列でDeskError発生
def test_create_project_form_tc5(request, project_service, ticket_service):
    # テストID: TC5
    name = ""
    slug = "project-empty"
    # create_projectがDeskErrorをraiseするよう設定
    project_service.create_project.side_effect = DeskError("name is empty")
    # TemplateResponseの返却をモック
    templates.TemplateResponse.return_value = "template_response"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert result == "template_response"
    templates.TemplateResponse.assert_called_once()
    args, kwargs = templates.TemplateResponse.call_args
    assert kwargs["status_code"] == 400
    assert "error" in kwargs["context"]
    assert "name is empty" in kwargs["context"]["error"]

# TC6: nameがNoneの場合（Form(...), なのでリクエスト時点で400エラー）
def test_create_project_form_tc6(request, project_service, ticket_service):
    # テストID: TC6
    name = None
    slug = "project-none"
    # Form(...), なのでFastAPIのバリデーションで400になるが、直接呼び出しの場合はTypeError/ValueError
    with pytest.raises(TypeError):
        create_project_form(request, name, slug, project_service, ticket_service)

# TC7: slugがNoneの場合
def test_create_project_form_tc7(request, project_service, ticket_service):
    # テストID: TC7
    name = "プロジェクトA"
    slug = None
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC8: nameがint型（型不一致）
def test_create_project_form_tc8(request, project_service, ticket_service):
    # テストID: TC8
    name = 1
    slug = "project-int"
    with pytest.raises(TypeError):
        create_project_form(request, name, slug, project_service, ticket_service)

# TC9: slugがint型（型不一致）
def test_create_project_form_tc9(request, project_service, ticket_service):
    # テストID: TC9
    name = "プロジェクトA"
    slug = 1
    with pytest.raises(TypeError):
        create_project_form(request, name, slug, project_service, ticket_service)

# TC10: create_projectでDeskError発生
def test_create_project_form_tc10(request, project_service, ticket_service):
    # テストID: TC10
    name = "プロジェクトA"
    slug = "project-a"
    project_service.create_project.side_effect = DeskError("error in create_project")
    templates.TemplateResponse.return_value = "template_response"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert result == "template_response"
    templates.TemplateResponse.assert_called_once()
    args, kwargs = templates.TemplateResponse.call_args
    assert kwargs["status_code"] == 400
    assert "error" in kwargs["context"]
    assert "error in create_project" in kwargs["context"]["error"]

# TC11: slug未入力かつcreate_projectでDeskError発生
def test_create_project_form_tc11(request, project_service, ticket_service):
    # テストID: TC11
    name = "プロジェクトA"
    slug = ""
    project_service.create_project.side_effect = DeskError("error in create_project")
    templates.TemplateResponse.return_value = "template_response"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert result == "template_response"
    templates.TemplateResponse.assert_called_once()
    args, kwargs = templates.TemplateResponse.call_args
    assert kwargs["status_code"] == 400
    assert "error" in kwargs["context"]
    assert "error in create_project" in kwargs["context"]["error"]

# TC12: nameとslug両方空文字列でDeskError発生
def test_create_project_form_tc12(request, project_service, ticket_service):
    # テストID: TC12
    name = ""
    slug = ""
    project_service.create_project.side_effect = DeskError("both empty")
    templates.TemplateResponse.return_value = "template_response"
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert result == "template_response"
    templates.TemplateResponse.assert_called_once()
    args, kwargs = templates.TemplateResponse.call_args
    assert kwargs["status_code"] == 400
    assert "error" in kwargs["context"]
    assert "both empty" in kwargs["context"]["error"]

# TC13: 長いプロジェクト名かつslug未入力
def test_create_project_form_tc13(request, project_service, ticket_service):
    # テストID: TC13
    name = "a" * 100
    slug = ""
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC14: チケット一覧が空の場合
def test_create_project_form_tc14(request, project_service, ticket_service):
    # テストID: TC14
    name = "プロジェクトA"
    slug = "project-a"
    ticket_service.list_tickets.return_value = []
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"

# TC15: プロジェクト一覧が空の場合
def test_create_project_form_tc15(request, project_service, ticket_service):
    # テストID: TC15
    name = "プロジェクトA"
    slug = "project-a"
    project_service.list_projects.return_value = []
    result = create_project_form(request, name, slug, project_service, ticket_service)
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == "/projects"
```
