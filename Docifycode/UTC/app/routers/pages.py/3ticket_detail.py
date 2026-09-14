import pytest

# --- モッククラス定義 ---
class TicketNotFound(Exception):
    pass

class TicketStatus:
    # ダミーEnum
    OPEN = "open"
    CLOSED = "closed"
    @classmethod
    def __iter__(cls):
        return iter([cls.OPEN, cls.CLOSED])

class Label:
    def __init__(self, id):
        self.id = id

class Member:
    pass

class Project:
    def __init__(self, archived=False):
        self.archived = archived

class Ticket:
    def __init__(self, label_ids=None):
        self.label_ids = label_ids or []

class Request:
    pass

class HTMLResponse:
    pass

class TemplateResponse:
    def __init__(self, request, template_name, context, status_code=200):
        self.request = request
        self.template_name = template_name
        self.context = context
        self.status_code = status_code

# --- テンプレートモック ---
class TemplatesMock:
    def TemplateResponse(self, request, template_name, context, status_code=200):
        return TemplateResponse(request, template_name, context, status_code)

templates = TemplatesMock()

# --- サービスモック ---
class TicketServiceMock:
    def __init__(self, tickets_dict=None, raise_not_found_ids=None):
        self.tickets_dict = tickets_dict or {}
        self.raise_not_found_ids = raise_not_found_ids or set()
    def get_ticket(self, ticket_id):
        if ticket_id in self.raise_not_found_ids or ticket_id not in self.tickets_dict:
            raise TicketNotFound()
        return self.tickets_dict[ticket_id]

class MemberServiceMock:
    def __init__(self, members=None):
        self.members = members if members is not None else [Member()]
    def list_members(self, active=True):
        return self.members

class ProjectServiceMock:
    def __init__(self, projects=None):
        self.projects = projects if projects is not None else [Project()]
    def list_projects(self):
        return self.projects

class LabelServiceMock:
    def __init__(self, labels=None):
        self.labels = labels if labels is not None else [Label(1), Label(2)]
    def list_labels(self):
        return self.labels

# --- テスト対象関数（直接コピー） ---
def ticket_detail(
    ticket_id: int,
    request: Request,
    tickets,
    members,
    projects,
    labels,
):
    try:
        ticket = tickets.get_ticket(ticket_id)
    except TicketNotFound:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            {"resource": "ticket", "item_id": ticket_id},
            status_code=404,
        )
    label_map = {label.id: label for label in labels.list_labels()}
    return templates.TemplateResponse(
        request,
        "ticket_detail.html",
        {
            "ticket": ticket,
            "statuses": list(TicketStatus),
            "members": members.list_members(active=True),
            "projects": [project for project in projects.list_projects() if not project.archived],
            "labels": labels.list_labels(),
            "ticket_labels": [label_map[label_id] for label_id in ticket.label_ids if label_id in label_map],
            "error": None,
        },
    )

# --- テストケース ---
# TC1: 正常系: 存在するチケットIDで全ての依存サービスが正常
def test_TC1_ticket_detail_normal():
    # TC1
    ticket = Ticket(label_ids=[1, 2])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock([Member()])
    projects = ProjectServiceMock([Project(archived=False)])
    labels = LabelServiceMock([Label(1), Label(2)])
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    # チケット詳細テンプレートが返ること
    assert resp.template_name == "ticket_detail.html"
    assert resp.context["ticket"] == ticket
    assert resp.status_code == 200

# TC2: 異常系: 存在しないチケットID（境界値）
def test_TC2_ticket_detail_not_found_boundary():
    # TC2
    tickets = TicketServiceMock({}, raise_not_found_ids={0})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(0, request, tickets, members, projects, labels)
    assert resp.template_name == "not_found.html"
    assert resp.status_code == 404
    assert resp.context["item_id"] == 0

# TC3: 異常系: 存在しないチケットID（負の値）
def test_TC3_ticket_detail_not_found_negative():
    # TC3
    tickets = TicketServiceMock({}, raise_not_found_ids={-1})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(-1, request, tickets, members, projects, labels)
    assert resp.template_name == "not_found.html"
    assert resp.status_code == 404
    assert resp.context["item_id"] == -1

# TC4: 異常系: 存在しないチケットID（非常に大きい値）
def test_TC4_ticket_detail_not_found_large():
    # TC4
    tickets = TicketServiceMock({}, raise_not_found_ids={999999})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(999999, request, tickets, members, projects, labels)
    assert resp.template_name == "not_found.html"
    assert resp.status_code == 404
    assert resp.context["item_id"] == 999999

# TC5: 異常系: ticket_idが文字列型（型不一致）
def test_TC5_ticket_detail_ticket_id_str():
    # TC5
    tickets = TicketServiceMock()
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    with pytest.raises(TypeError):
        ticket_detail("abc", request, tickets, members, projects, labels)

# TC6: 異常系: ticket_idがNone（型不一致）
def test_TC6_ticket_detail_ticket_id_none():
    # TC6
    tickets = TicketServiceMock()
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    with pytest.raises(TypeError):
        ticket_detail(None, request, tickets, members, projects, labels)

# TC7: 異常系: requestが不正な型やNone
@pytest.mark.parametrize("bad_request", [None, 123, "req"])
def test_TC7_ticket_detail_request_invalid(bad_request):
    # TC7
    tickets = TicketServiceMock({1: Ticket()})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    with pytest.raises(TypeError):
        ticket_detail(1, bad_request, tickets, members, projects, labels)

# TC8: 異常系: ticketsがNone
def test_TC8_ticket_detail_tickets_none():
    # TC8
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    with pytest.raises(TypeError):
        ticket_detail(1, request, None, members, projects, labels)

# TC9: 異常系: membersがNone
def test_TC9_ticket_detail_members_none():
    # TC9
    tickets = TicketServiceMock({1: Ticket()})
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    with pytest.raises(TypeError):
        ticket_detail(1, request, tickets, None, projects, labels)

# TC10: 異常系: projectsがNone
def test_TC10_ticket_detail_projects_none():
    # TC10
    tickets = TicketServiceMock({1: Ticket()})
    members = MemberServiceMock()
    labels = LabelServiceMock()
    request = Request()
    with pytest.raises(TypeError):
        ticket_detail(1, request, tickets, members, None, labels)

# TC11: 異常系: labelsがNone
def test_TC11_ticket_detail_labels_none():
    # TC11
    tickets = TicketServiceMock({1: Ticket()})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    request = Request()
    with pytest.raises(TypeError):
        ticket_detail(1, request, tickets, members, projects, None)

# TC12: 正常系: labels.list_labels()が空リスト
def test_TC12_ticket_detail_labels_empty():
    # TC12
    ticket = Ticket(label_ids=[1, 2])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock(labels=[])
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "ticket_detail.html"
    assert resp.context["labels"] == []
    assert resp.context["ticket_labels"] == []

# TC13: 正常系: members.list_members(active=True)が空リスト
def test_TC13_ticket_detail_members_empty():
    # TC13
    ticket = Ticket(label_ids=[1])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock(members=[])
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "ticket_detail.html"
    assert resp.context["members"] == []

# TC14: 正常系: projects.list_projects()が空リスト
def test_TC14_ticket_detail_projects_empty():
    # TC14
    ticket = Ticket(label_ids=[1])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock()
    projects = ProjectServiceMock(projects=[])
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "ticket_detail.html"
    assert resp.context["projects"] == []

# TC15: 異常系: tickets.get_ticket(ticket_id)がTicketNotFoundを返す場合
def test_TC15_ticket_detail_ticket_not_found():
    # TC15
    tickets = TicketServiceMock({}, raise_not_found_ids={1})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "not_found.html"
    assert resp.status_code == 404
    assert resp.context["item_id"] == 1

# TC16: 正常系: projects.list_projects()の全てのprojectがarchived=Trueでprojectsリストが空
def test_TC16_ticket_detail_projects_all_archived():
    # TC16
    ticket = Ticket(label_ids=[1])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock()
    projects = ProjectServiceMock(projects=[Project(archived=True), Project(archived=True)])
    labels = LabelServiceMock()
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "ticket_detail.html"
    assert resp.context["projects"] == []

# TC17: 正常系: ticket.label_idsが空リスト
def test_TC17_ticket_detail_ticket_label_ids_empty():
    # TC17
    ticket = Ticket(label_ids=[])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock([Label(1), Label(2)])
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "ticket_detail.html"
    assert resp.context["ticket_labels"] == []

# TC18: 正常系: ticket.label_idsの一部がlabels.list_labels()に存在しない場合
def test_TC18_ticket_detail_ticket_label_ids_partial_missing():
    # TC18
    ticket = Ticket(label_ids=[1, 2, 3])
    tickets = TicketServiceMock({1: ticket})
    members = MemberServiceMock()
    projects = ProjectServiceMock()
    labels = LabelServiceMock([Label(1), Label(2)])  # label_id=3は存在しない
    request = Request()
    resp = ticket_detail(1, request, tickets, members, projects, labels)
    assert resp.template_name == "ticket_detail.html"
    # ticket_labelsには存在するlabelのみ含まれる
    assert [label.id for label in resp.context["ticket_labels"]] == [1, 2]
```
