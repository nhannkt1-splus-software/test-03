import pytest

# テスト用のモッククラス
class MockProjectService:
    def __init__(self, projects=None, raise_exc=False):
        self._projects = projects
        self._raise_exc = raise_exc

    def list_projects(self):
        if self._raise_exc:
            raise Exception("ProjectService error")
        return self._projects

class MockTicketService:
    def __init__(self, tickets=None, raise_exc=False):
        self._tickets = tickets
        self._raise_exc = raise_exc

    def list_tickets(self):
        if self._raise_exc:
            raise Exception("TicketService error")
        return self._tickets

# テンプレートレスポンスのモック
class MockTemplateResponse:
    def __init__(self, request, template_name, context):
        self.request = request
        self.template_name = template_name
        self.context = context

# テンプレートのモック
class MockTemplates:
    def TemplateResponse(self, request, template_name, context):
        return MockTemplateResponse(request, template_name, context)

# Requestのモック
class MockRequest:
    pass

# projects_page関数のテスト用ラッパー
def projects_page(request, projects, tickets):
    # テンプレートをモックに置き換え
    templates = MockTemplates()
    return templates.TemplateResponse(
        request,
        "projects.html",
        {
            "projects": projects.list_projects(),
            "tickets": tickets.list_tickets(),
            "error": None,
        },
    )

# --- テストケース ---

# TC1: 正常系：全ての入力が正しい型で、プロジェクトとチケットが複数件返るケース
def test_projects_page_TC1():
    # TC1
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"},
        {"id": 2, "name": "プロジェクトB"}
    ])
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"},
        {"id": 11, "title": "チケット2"}
    ])
    request = MockRequest()
    resp = projects_page(request, projects, tickets)
    # 期待値確認
    assert resp.context["projects"] == [
        {"id": 1, "name": "プロジェクトA"},
        {"id": 2, "name": "プロジェクトB"}
    ]
    assert resp.context["tickets"] == [
        {"id": 10, "title": "チケット1"},
        {"id": 11, "title": "チケット2"}
    ]
    assert resp.context["error"] is None

# TC2: 正常系：プロジェクトが空リストの場合
def test_projects_page_TC2():
    # TC2
    projects = MockProjectService([])
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"},
        {"id": 11, "title": "チケット2"}
    ])
    request = MockRequest()
    resp = projects_page(request, projects, tickets)
    assert resp.context["projects"] == []
    assert resp.context["tickets"] == [
        {"id": 10, "title": "チケット1"},
        {"id": 11, "title": "チケット2"}
    ]
    assert resp.context["error"] is None

# TC3: 正常系：チケットが空リストの場合
def test_projects_page_TC3():
    # TC3
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"},
        {"id": 2, "name": "プロジェクトB"}
    ])
    tickets = MockTicketService([])
    request = MockRequest()
    resp = projects_page(request, projects, tickets)
    assert resp.context["projects"] == [
        {"id": 1, "name": "プロジェクトA"},
        {"id": 2, "name": "プロジェクトB"}
    ]
    assert resp.context["tickets"] == []
    assert resp.context["error"] is None

# TC4: 正常系：プロジェクトとチケットが両方とも空リストの場合
def test_projects_page_TC4():
    # TC4
    projects = MockProjectService([])
    tickets = MockTicketService([])
    request = MockRequest()
    resp = projects_page(request, projects, tickets)
    assert resp.context["projects"] == []
    assert resp.context["tickets"] == []
    assert resp.context["error"] is None

# TC5: 異常系：ProjectService.list_projects()が例外を投げる場合
def test_projects_page_TC5():
    # TC5
    projects = MockProjectService(raise_exc=True)
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"},
        {"id": 11, "title": "チケット2"}
    ])
    request = MockRequest()
    with pytest.raises(Exception):
        projects_page(request, projects, tickets)

# TC6: 異常系：TicketService.list_tickets()が例外を投げる場合
def test_projects_page_TC6():
    # TC6
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"},
        {"id": 2, "name": "プロジェクトB"}
    ])
    tickets = MockTicketService(raise_exc=True)
    request = MockRequest()
    with pytest.raises(Exception):
        projects_page(request, projects, tickets)

# TC7: 異常系：RequestがNoneの場合
def test_projects_page_TC7():
    # TC7
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = None
    with pytest.raises(TypeError):
        projects_page(request, projects, tickets)

# TC8: 異常系：Requestが不正な型の場合（整数）
def test_projects_page_TC8():
    # TC8
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = 123
    with pytest.raises(TypeError):
        projects_page(request, projects, tickets)

# TC9: 異常系：ProjectServiceがNoneの場合
def test_projects_page_TC9():
    # TC9
    projects = None
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = MockRequest()
    with pytest.raises(AttributeError):
        projects_page(request, projects, tickets)

# TC10: 異常系：ProjectServiceが不正な型の場合（整数）
def test_projects_page_TC10():
    # TC10
    projects = 123
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = MockRequest()
    with pytest.raises(AttributeError):
        projects_page(request, projects, tickets)

# TC11: 異常系：TicketServiceがNoneの場合
def test_projects_page_TC11():
    # TC11
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    tickets = None
    request = MockRequest()
    with pytest.raises(AttributeError):
        projects_page(request, projects, tickets)

# TC12: 異常系：TicketServiceが不正な型の場合（整数）
def test_projects_page_TC12():
    # TC12
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    tickets = 456
    request = MockRequest()
    with pytest.raises(AttributeError):
        projects_page(request, projects, tickets)

# TC13: 異常系：ProjectServiceインスタンスにlist_projectsメソッドが存在しない場合
def test_projects_page_TC13():
    # TC13
    class NoListProjects:
        pass
    projects = NoListProjects()
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = MockRequest()
    with pytest.raises(AttributeError):
        projects_page(request, projects, tickets)

# TC14: 異常系：TicketServiceインスタンスにlist_ticketsメソッドが存在しない場合
def test_projects_page_TC14():
    # TC14
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    class NoListTickets:
        pass
    tickets = NoListTickets()
    request = MockRequest()
    with pytest.raises(AttributeError):
        projects_page(request, projects, tickets)

# TC15: 異常系：Requestが空文字列の場合
def test_projects_page_TC15():
    # TC15
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = ""
    with pytest.raises(TypeError):
        projects_page(request, projects, tickets)

# TC16: 正常系：projectsとticketsが1件ずつ返る場合
def test_projects_page_TC16():
    # TC16
    projects = MockProjectService([
        {"id": 1, "name": "プロジェクトA"}
    ])
    tickets = MockTicketService([
        {"id": 10, "title": "チケット1"}
    ])
    request = MockRequest()
    resp = projects_page(request, projects, tickets)
    assert resp.context["projects"] == [
        {"id": 1, "name": "プロジェクトA"}
    ]
    assert resp.context["tickets"] == [
        {"id": 10, "title": "チケット1"}
    ]
    assert resp.context["error"] is None

# TC17: 正常系：projectsとticketsが空リスト、errorがNoneで返る場合
def test_projects_page_TC17():
    # TC17
    projects = MockProjectService([])
    tickets = MockTicketService([])
    request = MockRequest()
    resp = projects_page(request, projects, tickets)
    assert resp.context["projects"] == []
    assert resp.context["tickets"] == []
    assert resp.context["error"] is None