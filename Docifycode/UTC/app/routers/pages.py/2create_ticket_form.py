import pytest

# テスト用のモッククラスと例外
class DeskError(Exception):
    pass

class Priority:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Ticket:
    def __init__(self, id):
        self.id = id

class TicketService:
    def __init__(self, error_case=None, invalid_assignee=None, invalid_project=None):
        self.error_case = error_case
        self.invalid_assignee = invalid_assignee
        self.invalid_project = invalid_project

    def create_ticket(self, title, description, priority, assignee, project_id):
        # TC2: titleが空文字の場合
        if title == "":
            raise DeskError("Title is required")
        # TC4: priorityがPriority型でない場合
        if priority not in [Priority.LOW, Priority.MEDIUM, Priority.HIGH]:
            raise TypeError("Invalid priority type")
        # TC5: project_idがint変換できない場合
        if isinstance(project_id, str) and not project_id.isdigit():
            raise ValueError("Invalid project_id")
        # TC14: assigneeが存在しないユーザーの場合
        if self.invalid_assignee and assignee == self.invalid_assignee:
            raise DeskError("Assignee not found")
        # TC15: project_idが存在しないプロジェクトIDの場合
        if self.invalid_project and project_id == self.invalid_project:
            raise DeskError("Project not found")
        # TC18: tickets.create_ticketでDeskErrorが発生する場合
        if self.error_case:
            raise DeskError("Ticket creation error")
        return Ticket(id=1)

    def list_tickets(self):
        return []

class MemberService:
    def list_members(self, active=True):
        return []

class ProjectService:
    def list_projects(self):
        return []

class Request:
    pass

class templates:
    @staticmethod
    def TemplateResponse(request, template_name, context, status_code):
        return {"template": template_name, "context": context, "status_code": status_code}

def _board_context(tickets, members, projects, error, **kwargs):
    return {"tickets": tickets, "members": members, "projects": projects, "error": error}

from starlette.responses import RedirectResponse

# テスト対象関数
def create_ticket_form(
    request,
    title,
    description="",
    priority=Priority.MEDIUM,
    assignee="",
    project_id="",
    tickets=None,
    members=None,
    projects=None,
):
    parsed_project = int(project_id) if project_id else None
    try:
        ticket = tickets.create_ticket(
            title,
            description,
            priority,
            assignee or None,
            parsed_project,
        )
        return RedirectResponse(url=f"/tickets/{ticket.id}", status_code=303)
    except DeskError as exc:
        return templates.TemplateResponse(
            request,
            "index.html",
            _board_context(
                tickets.list_tickets(),
                members.list_members(active=True),
                projects.list_projects(),
                str(exc),
            )
            | {"q": ""},
            status_code=400,
        )

# テストケース
@pytest.mark.parametrize("test_id,params,expected", [
    # --- TC1 ---
    # 正常系：全ての入力が有効な値
    ("TC1", {
        "assignee": "user1",
        "description": "有効な説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "有効なタイトル"
    }, RedirectResponse),

    # --- TC2 ---
    # 異常系：titleが空文字の場合
    ("TC2", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.LOW,
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": ""
    }, DeskError),

    # --- TC3 ---
    # 正常系：descriptionが空文字の場合
    ("TC3", {
        "assignee": "",
        "description": "",
        "members": MemberService(),
        "priority": Priority.HIGH,
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC4 ---
    # 異常系：priorityが不正な値（型違い）
    ("TC4", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": "invalid_priority",
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, TypeError),

    # --- TC5 ---
    # 異常系：project_idが数値でない文字列
    ("TC5", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "abc",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, ValueError),

    # --- TC6 ---
    # 正常系：project_idが空文字の場合
    ("TC6", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC7 ---
    # 正常系：project_idが非常に大きい数値文字列
    ("TC7", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "999999999999999999999999",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC8 ---
    # 正常系：assigneeが有効なユーザー
    ("TC8", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC9 ---
    # 正常系：assigneeが空文字
    ("TC9", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC10 ---
    # 異常系：titleがint型（型違い）
    ("TC10", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": 123
    }, TypeError),

    # --- TC11 ---
    # 異常系：descriptionがint型（型違い）
    ("TC11", {
        "assignee": "",
        "description": 123,
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, TypeError),

    # --- TC12 ---
    # 異常系：assigneeがint型（型違い）
    ("TC12", {
        "assignee": 123,
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, TypeError),

    # --- TC13 ---
    # 正常系：project_idがint型（int型でもint(project_id)可能）
    ("TC13", {
        "assignee": "",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": 123,
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC14 ---
    # 異常系：assigneeが存在しないユーザーの場合
    ("TC14", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(invalid_assignee="user1"),
        "title": "タイトル"
    }, DeskError),

    # --- TC15 ---
    # 異常系：project_idが存在しないプロジェクトIDの場合
    ("TC15", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "999999999999999999999999",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(invalid_project=999999999999999999999999),
        "title": "タイトル"
    }, DeskError),

    # --- TC16 ---
    # 正常系：タイトルが非常に長い場合
    ("TC16", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "a" * 1000
    }, RedirectResponse),

    # --- TC17 ---
    # 正常系：descriptionが非常に長い場合
    ("TC17", {
        "assignee": "user1",
        "description": "a" * 1000,
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, RedirectResponse),

    # --- TC18 ---
    # 異常系：tickets.create_ticketでDeskErrorが発生する場合
    ("TC18", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(error_case=True),
        "title": "タイトル"
    }, DeskError),

    # --- TC19 ---
    # 異常系：ticketsがNoneの場合
    ("TC19", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": None,
        "title": "タイトル"
    }, AttributeError),

    # --- TC20 ---
    # 異常系：membersがNoneの場合
    ("TC20", {
        "assignee": "user1",
        "description": "説明",
        "members": None,
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": ProjectService(),
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, AttributeError),

    # --- TC21 ---
    # 異常系：projectsがNoneの場合
    ("TC21", {
        "assignee": "user1",
        "description": "説明",
        "members": MemberService(),
        "priority": Priority.MEDIUM,
        "project_id": "1",
        "projects": None,
        "request": Request(),
        "tickets": TicketService(),
        "title": "タイトル"
    }, AttributeError),
])
def test_create_ticket_form(test_id, params, expected):
    # テストIDをコメントで明示
    # --- {test_id} ---
    if expected in (DeskError, TypeError, ValueError, AttributeError):
        with pytest.raises(expected):
            create_ticket_form(
                request=params["request"],
                title=params["title"],
                description=params["description"],
                priority=params["priority"],
                assignee=params["assignee"],
                project_id=params["project_id"],
                tickets=params["tickets"],
                members=params["members"],
                projects=params["projects"],
            )
    else:
        result = create_ticket_form(
            request=params["request"],
            title=params["title"],
            description=params["description"],
            priority=params["priority"],
            assignee=params["assignee"],
            project_id=params["project_id"],
            tickets=params["tickets"],
            members=params["members"],
            projects=params["projects"],
        )
        # 正常系：RedirectResponseまたはテンプレートレスポンス
        if expected is RedirectResponse:
            # starlette.responses.RedirectResponse型かどうか
            assert isinstance(result, RedirectResponse)
        else:
            # テンプレートレスポンス（dict型）かどうか
            assert isinstance(result, dict)