import pytest
from unittest.mock import Mock, create_autospec
from starlette.responses import RedirectResponse

# --- テスト用ダミークラス定義 ---
class DeskError(Exception):
    pass

class Request:
    pass

class TicketService:
    def set_project(self, ticket_id, project_id):
        pass

class MemberService:
    pass

class ProjectService:
    pass

class LabelService:
    pass

# --- テスト対象関数のimport ---
import sys

# テスト対象関数をimportするためのヘルパー
def import_target():
    # テスト対象関数がグローバルスコープにある場合
    if "set_project_form" in globals():
        return globals()["set_project_form"]
    # そうでなければ、モジュールからimport
    import importlib
    mod = importlib.import_module("main")  # main.py等にある場合は修正
    return getattr(mod, "set_project_form")

set_project_form = import_target()

# --- _ticket_errorのモック ---
def _ticket_error(request, ticket_id, msg, tickets, members, projects, labels):
    # エラー時の返却値を識別できるようにする
    return {
        "error": True,
        "request": request,
        "ticket_id": ticket_id,
        "msg": msg,
        "tickets": tickets,
        "members": members,
        "projects": projects,
        "labels": labels,
    }

# テスト対象関数のグローバル名前空間を書き換え
set_project_form.__globals__["_ticket_error"] = _ticket_error
set_project_form.__globals__["DeskError"] = DeskError

# --- テストケース ---

# TC1: 正常系 有効なticket_idと有効なproject_id
def test_TC1():
    # TC1
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "123"
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    # 正常時はRedirectResponse
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == f"/tickets/{ticket_id}"
    tickets.set_project.assert_called_once_with(ticket_id, 123)

# TC2: 正常系 project_idが空文字
def test_TC2():
    # TC2
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = ""
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == f"/tickets/{ticket_id}"
    tickets.set_project.assert_called_once_with(ticket_id, None)

# TC3: ticket_id=0（存在しない）→DeskError
def test_TC3():
    # TC3
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("not found")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 0
    project_id = "123"
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "not found"

# TC4: ticket_id=-1（負の値）→DeskError
def test_TC4():
    # TC4
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("not found")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = -1
    project_id = "123"
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "not found"

# TC5: ticket_id=999999（大きい値）→DeskError
def test_TC5():
    # TC5
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("not found")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 999999
    project_id = "123"
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "not found"

# TC6: ticket_idがstr型（型不一致）→TypeError
def test_TC6():
    # TC6
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = "abc"
    project_id = "123"
    with pytest.raises(TypeError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )

# TC7: ticket_idがNone（型不一致）→TypeError
def test_TC7():
    # TC7
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = None
    project_id = "123"
    with pytest.raises(TypeError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )

# TC8: project_idが数字以外の文字列→ValueError
def test_TC8():
    # TC8
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "abc"
    with pytest.raises(ValueError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )

# TC9: project_idがNone→TypeError
def test_TC9():
    # TC9
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = None
    with pytest.raises(TypeError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )

# TC10: requestが不正な型→TypeError
def test_TC10():
    # TC10
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = 123  # 不正な型
    ticket_id = 1
    project_id = "123"
    with pytest.raises(TypeError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )

# TC11: ticketsが不正な型→TypeError
def test_TC11():
    # TC11
    tickets = 123  # 不正な型
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "123"
    with pytest.raises(AttributeError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )

# TC12: membersが不正な型→TypeError
def test_TC12():
    # TC12
    tickets = create_autospec(TicketService)
    members = 123  # 不正な型
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "123"
    # membersは直接使われないが、_ticket_errorで使われるため、DeskError発生させる
    tickets.set_project.side_effect = DeskError("err")
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["members"] == members

# TC13: projectsが不正な型→TypeError
def test_TC13():
    # TC13
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = 123  # 不正な型
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "123"
    tickets.set_project.side_effect = DeskError("err")
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["projects"] == projects

# TC14: labelsが不正な型→TypeError
def test_TC14():
    # TC14
    tickets = create_autospec(TicketService)
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = 123  # 不正な型
    request = Request()
    ticket_id = 1
    project_id = "123"
    tickets.set_project.side_effect = DeskError("err")
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["labels"] == labels

# TC15: tickets.set_projectがDeskError
def test_TC15():
    # TC15
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("業務エラー")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "123"
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "業務エラー"

# TC16: project_idが空文字でtickets.set_projectがDeskError
def test_TC16():
    # TC16
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("業務エラー")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = ""
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "業務エラー"

# TC17: ticket_id=0, project_id=""でDeskError
def test_TC17():
    # TC17
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("not found")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 0
    project_id = ""
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "not found"

# TC18: ticket_id=-1, project_id=""でDeskError
def test_TC18():
    # TC18
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("not found")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = -1
    project_id = ""
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "not found"

# TC19: ticket_id=999999, project_id=""でDeskError
def test_TC19():
    # TC19
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("not found")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 999999
    project_id = ""
    result = set_project_form(
        ticket_id=ticket_id,
        request=request,
        project_id=project_id,
        tickets=tickets,
        members=members,
        projects=projects,
        labels=labels,
    )
    assert result["error"] is True
    assert result["msg"] == "not found"

# TC20: project_idが数字以外の文字列、tickets.set_projectがDeskErrorでもValueError優先
def test_TC20():
    # TC20
    tickets = create_autospec(TicketService)
    tickets.set_project.side_effect = DeskError("should not be called")
    members = create_autospec(MemberService)
    projects = create_autospec(ProjectService)
    labels = create_autospec(LabelService)
    request = Request()
    ticket_id = 1
    project_id = "abc"
    with pytest.raises(ValueError):
        set_project_form(
            ticket_id=ticket_id,
            request=request,
            project_id=project_id,
            tickets=tickets,
            members=members,
            projects=projects,
            labels=labels,
        )