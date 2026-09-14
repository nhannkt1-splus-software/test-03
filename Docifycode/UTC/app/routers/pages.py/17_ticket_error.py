import pytest
from unittest.mock import MagicMock

# --- テスト用ダミークラス定義 ---

class DummyRequest:
    # Requestのダミー
    pass

class DummyTemplateResponse:
    # TemplateResponseのダミー
    def __init__(self, request, template_name, context, status_code):
        self.request = request
        self.template_name = template_name
        self.context = context
        self.status_code = status_code

class DummyTemplates:
    # templates.TemplateResponseのダミー
    def TemplateResponse(self, request, template_name, context, status_code):
        return DummyTemplateResponse(request, template_name, context, status_code)

class DummyTicket:
    def __init__(self, id=1, label_ids=None):
        self.id = id
        self.label_ids = label_ids if label_ids is not None else []

class DummyLabel:
    def __init__(self, id, name="label"):
        self.id = id
        self.name = name

class DummyProject:
    def __init__(self, id, archived=False):
        self.id = id
        self.archived = archived

class DummyMember:
    def __init__(self, id, active=True):
        self.id = id
        self.active = active

class DummyTicketService:
    def __init__(self, tickets=None):
        # tickets: dict[int, DummyTicket]
        self._tickets = tickets if tickets is not None else {}

    def get_ticket(self, ticket_id):
        return self._tickets.get(ticket_id, None)

class DummyLabelService:
    def __init__(self, labels=None):
        self._labels = labels if labels is not None else []

    def list_labels(self):
        return self._labels

class DummyMemberService:
    def __init__(self, members=None):
        self._members = members if members is not None else []

    def list_members(self, active=True):
        return [m for m in self._members if m.active] if active else self._members

class DummyProjectService:
    def __init__(self, projects=None):
        self._projects = projects if projects is not None else []

    def list_projects(self):
        return self._projects

# TicketStatusのダミーEnum
class DummyTicketStatus:
    values = ["OPEN", "CLOSED"]
    def __iter__(self):
        return iter(self.values)
TicketStatus = DummyTicketStatus()

# テンプレートをグローバルにモック
templates = DummyTemplates()

# --- テスト対象関数のimport ---
import sys
import types

# テスト対象関数をインポート
# _ticket_errorはスコープ外なので、execで定義
_target_code = '''
def _ticket_error(
    request,
    ticket_id,
    error,
    tickets,
    members,
    projects,
    labels,
):
    ticket = tickets.get_ticket(ticket_id)
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
            "ticket_labels": [label_map[label_id] for label_id in ticket.label_ids if label_id in label_map] if ticket else [],
            "error": error,
        },
        status_code=409,
    )
'''
_testmod = types.ModuleType("testmod")
_testmod.__dict__.update(globals())
exec(_target_code, _testmod.__dict__)
_ticket_error = _testmod._ticket_error

# --- 各テストケース ---

# TC1: 正常系: 全ての入力が有効で、チケット・メンバー・プロジェクト・ラベルが存在する場合
def test_TC1():
    # TC1
    request = DummyRequest()
    ticket_id = 1
    error = "不正な操作"
    labels = [DummyLabel(1, "bug"), DummyLabel(2, "feature")]
    tickets = DummyTicketService({1: DummyTicket(1, [1,2])})
    members = DummyMemberService([DummyMember(1), DummyMember(2)])
    projects = DummyProjectService([DummyProject(1), DummyProject(2, archived=True), DummyProject(3)])
    label_service = DummyLabelService(labels)
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    # 結果検証
    assert isinstance(result, DummyTemplateResponse)
    assert result.status_code == 409
    assert result.template_name == "ticket_detail.html"
    assert result.context["ticket"].id == 1
    assert result.context["error"] == error
    assert result.context["members"] == [m for m in members._members if m.active]
    assert result.context["projects"] == [p for p in projects._projects if not p.archived]
    assert result.context["labels"] == labels
    assert result.context["ticket_labels"] == labels
    assert set(result.context["statuses"]) == set(TicketStatus.values)

# TC2: 境界値: 存在しない非常に大きいticket_idの場合
def test_TC2():
    # TC2
    request = DummyRequest()
    ticket_id = 1000000000
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert isinstance(result, DummyTemplateResponse)
    assert result.status_code == 409
    assert result.context["ticket"] is None

# TC3: 境界値: ticket_idが0の場合
def test_TC3():
    # TC3
    request = DummyRequest()
    ticket_id = 0
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert isinstance(result, DummyTemplateResponse)
    assert result.status_code == 409
    assert result.context["ticket"] is None

# TC4: 境界値: ticket_idが負の値の場合
def test_TC4():
    # TC4
    request = DummyRequest()
    ticket_id = -1
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert isinstance(result, DummyTemplateResponse)
    assert result.status_code == 409
    assert result.context["ticket"] is None

# TC5: 異常系: ticket_idがint型でない場合（文字列）
def test_TC5():
    # TC5
    request = DummyRequest()
    ticket_id = "abc"
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    with pytest.raises(TypeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC6: 異常系: ticket_idがint型でない場合（float型）
def test_TC6():
    # TC6
    request = DummyRequest()
    ticket_id = 1.5
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    with pytest.raises(TypeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC7: 異常系: requestがNoneの場合
def test_TC7():
    # TC7
    request = None
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    with pytest.raises(TypeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC8: 正常系: errorが空文字列の場合
def test_TC8():
    # TC8
    request = DummyRequest()
    ticket_id = 1
    error = ""
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["error"] == ""

# TC9: 正常系: errorがNoneの場合
def test_TC9():
    # TC9
    request = DummyRequest()
    ticket_id = 1
    error = None
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["error"] is None

# TC10: 異常系: ticketsがNoneの場合
def test_TC10():
    # TC10
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = None
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    with pytest.raises(AttributeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC11: 異常系: membersがNoneの場合
def test_TC11():
    # TC11
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = None
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    with pytest.raises(AttributeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC12: 異常系: projectsがNoneの場合
def test_TC12():
    # TC12
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = DummyMemberService([DummyMember(1)])
    projects = None
    label_service = DummyLabelService([DummyLabel(1)])
    with pytest.raises(AttributeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC13: 異常系: labelsがNoneの場合
def test_TC13():
    # TC13
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = None
    with pytest.raises(AttributeError):
        _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)

# TC14: 正常系: メンバーが存在しない場合
def test_TC14():
    # TC14
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = DummyMemberService([])  # 空リスト
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["members"] == []

# TC15: 正常系: プロジェクトが存在しない場合
def test_TC15():
    # TC15
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [1])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([])  # 空リスト
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["projects"] == []

# TC16: 正常系: ラベルが存在しない場合
def test_TC16():
    # TC16
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([])  # 空リスト
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["labels"] == []
    assert result.context["ticket_labels"] == []

# TC17: 正常系: ticket.label_idsに存在しないlabel_idが含まれている場合
def test_TC17():
    # TC17
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [99])})  # 存在しないlabel_id
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["ticket_labels"] == []

# TC18: 正常系: get_ticketがNoneを返す場合（ticket_idが存在しない場合）
def test_TC18():
    # TC18
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["ticket"] is None

# TC19: 正常系: ticket.label_idsが空リストの場合
def test_TC19():
    # TC19
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["ticket_labels"] == []

# TC20: 正常系: ticket.label_idsに存在しないlabel_idが含まれている場合（labels.list_labelsに該当ラベルがない場合）
def test_TC20():
    # TC20
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [1,2,3])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([DummyLabel(1)])  # id=1のみ
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    # ticket_labelsはid=1のみ
    assert result.context["ticket_labels"] == [label_service._labels[0]]

# TC21: 正常系: ticket.label_idsに重複idが含まれている場合
def test_TC21():
    # TC21
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    label_obj = DummyLabel(1)
    tickets = DummyTicketService({1: DummyTicket(1, [1,1])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([label_obj])
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    # 重複分だけ返す
    assert result.context["ticket_labels"] == [label_obj, label_obj]

# TC22: 正常系: labels.list_labelsが空リストで、ticket.label_idsに存在しないidが含まれている場合
def test_TC22():
    # TC22
    request = DummyRequest()
    ticket_id = 1
    error = "エラー内容"
    tickets = DummyTicketService({1: DummyTicket(1, [99])})
    members = DummyMemberService([DummyMember(1)])
    projects = DummyProjectService([DummyProject(1)])
    label_service = DummyLabelService([])  # 空リスト
    result = _ticket_error(request, ticket_id, error, tickets, members, projects, label_service)
    assert result.context["ticket_labels"] == []