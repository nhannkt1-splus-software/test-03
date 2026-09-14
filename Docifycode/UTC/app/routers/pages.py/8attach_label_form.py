import pytest
from unittest.mock import Mock, MagicMock, create_autospec
from starlette.responses import RedirectResponse

# --- テスト用ダミークラス・例外定義 ---

# DeskError例外のダミー定義
class DeskError(Exception):
    pass

# _ticket_errorのダミー定義
def _ticket_error(request, ticket_id, message, tickets, members, projects, labels):
    # エラー時の返却値を分かりやすくするため、dictで返す
    return {
        "error": message,
        "ticket_id": ticket_id,
        "request": request,
        "tickets": tickets,
        "members": members,
        "projects": projects,
        "labels": labels,
    }

# Requestのダミー
class DummyRequest:
    pass

# --- テスト対象関数のimport ---
# テスト対象関数がスコープ外の場合は、import文を調整してください
from types import SimpleNamespace

# テスト対象関数をimport
from your_module import attach_label_form  # ← your_moduleを実際のモジュール名に変更してください

# --- テストケース ---

# TC1, TC14: 正常系
@pytest.mark.parametrize("test_id, ticket_id, label_id", [
    # TC1
    ("TC1", 1, 2),
    # TC14
    ("TC14", 1, 2),
])
def test_attach_label_form_success(test_id, ticket_id, label_id):
    # 正常なサービスのモック
    labels = Mock()
    labels.attach = Mock()
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    # 実行
    result = attach_label_form(
        ticket_id=ticket_id,
        request=request,
        label_id=label_id,
        labels=labels,
        tickets=tickets,
        members=members,
        projects=projects,
    )
    # リダイレクトレスポンスであることを確認
    assert isinstance(result, RedirectResponse)
    assert result.status_code == 303
    assert result.headers["location"] == f"/tickets/{ticket_id}"

# TC2, TC3, TC4: ticket_idが不正な場合（DeskError発生）
@pytest.mark.parametrize("test_id, ticket_id", [
    # TC2
    ("TC2", 0),
    # TC3
    ("TC3", -1),
    # TC4
    ("TC4", 1000000),
])
def test_attach_label_form_ticket_id_invalid_deskerror(test_id, ticket_id):
    labels = Mock()
    # attachがDeskErrorを投げる
    labels.attach = Mock(side_effect=DeskError("invalid ticket_id"))
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    # 実行
    result = attach_label_form(
        ticket_id=ticket_id,
        request=request,
        label_id=2,
        labels=labels,
        tickets=tickets,
        members=members,
        projects=projects,
    )
    # _ticket_errorの返却値であることを確認
    assert isinstance(result, dict)
    assert result["error"] == "invalid ticket_id"
    assert result["ticket_id"] == ticket_id

# TC5, TC6: ticket_idが型不一致
@pytest.mark.parametrize("test_id, ticket_id", [
    # TC5
    ("TC5", "abc"),
    # TC6
    ("TC6", None),
])
def test_attach_label_form_ticket_id_type_error(test_id, ticket_id):
    labels = Mock()
    labels.attach = Mock()
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    # TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        attach_label_form(
            ticket_id=ticket_id,
            request=request,
            label_id=2,
            labels=labels,
            tickets=tickets,
            members=members,
            projects=projects,
        )

# TC7, TC8, TC9: label_idが不正な場合（DeskError発生）
@pytest.mark.parametrize("test_id, label_id", [
    # TC7
    ("TC7", 0),
    # TC8
    ("TC8", -5),
    # TC9
    ("TC9", 999999),
])
def test_attach_label_form_label_id_invalid_deskerror(test_id, label_id):
    labels = Mock()
    labels.attach = Mock(side_effect=DeskError("invalid label_id"))
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    # 実行
    result = attach_label_form(
        ticket_id=1,
        request=request,
        label_id=label_id,
        labels=labels,
        tickets=tickets,
        members=members,
        projects=projects,
    )
    assert isinstance(result, dict)
    assert result["error"] == "invalid label_id"
    assert result["ticket_id"] == 1

# TC10, TC11: label_idが型不一致
@pytest.mark.parametrize("test_id, label_id", [
    # TC10
    ("TC10", "xyz"),
    # TC11
    ("TC11", None),
])
def test_attach_label_form_label_id_type_error(test_id, label_id):
    labels = Mock()
    labels.attach = Mock()
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    with pytest.raises(TypeError):
        attach_label_form(
            ticket_id=1,
            request=request,
            label_id=label_id,
            labels=labels,
            tickets=tickets,
            members=members,
            projects=projects,
        )

# TC12: 不正なRequestオブジェクト
def test_attach_label_form_invalid_request_TC12():
    labels = Mock()
    labels.attach = Mock(side_effect=DeskError("request error"))
    tickets = Mock()
    members = Mock()
    projects = Mock()
    # 不正なRequestオブジェクト
    class InvalidRequest:
        pass
    request = InvalidRequest()
    result = attach_label_form(
        ticket_id=1,
        request=request,
        label_id=2,
        labels=labels,
        tickets=tickets,
        members=members,
        projects=projects,
    )
    assert isinstance(result, dict)
    assert result["error"] == "request error"
    assert result["request"] == request

# TC13: labels.attach()でDeskError例外が発生
def test_attach_label_form_labels_attach_raises_TC13():
    labels = Mock()
    labels.attach = Mock(side_effect=DeskError("attach error"))
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    result = attach_label_form(
        ticket_id=1,
        request=request,
        label_id=2,
        labels=labels,
        tickets=tickets,
        members=members,
        projects=projects,
    )
    assert isinstance(result, dict)
    assert result["error"] == "attach error"

# TC15: labels.attachが未実装またはNone
@pytest.mark.parametrize("test_id, attach_value", [
    # attachがNone
    ("TC15-1", None),
    # attachが存在しない
    ("TC15-2", "no_attr"),
])
def test_attach_label_form_labels_attach_missing_TC15(test_id, attach_value):
    labels = Mock()
    if attach_value == "no_attr":
        # attach属性自体を削除
        if hasattr(labels, "attach"):
            del labels.attach
    else:
        labels.attach = None
    tickets = Mock()
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    with pytest.raises(AttributeError):
        attach_label_form(
            ticket_id=1,
            request=request,
            label_id=2,
            labels=labels,
            tickets=tickets,
            members=members,
            projects=projects,
        )

# TC16: ticketsがNone
def test_attach_label_form_tickets_none_TC16():
    labels = Mock()
    labels.attach = Mock()
    tickets = None
    members = Mock()
    projects = Mock()
    request = DummyRequest()
    with pytest.raises(AttributeError):
        attach_label_form(
            ticket_id=1,
            request=request,
            label_id=2,
            labels=labels,
            tickets=tickets,
            members=members,
            projects=projects,
        )

# TC17: membersがNone
def test_attach_label_form_members_none_TC17():
    labels = Mock()
    labels.attach = Mock()
    tickets = Mock()
    members = None
    projects = Mock()
    request = DummyRequest()
    with pytest.raises(AttributeError):
        attach_label_form(
            ticket_id=1,
            request=request,
            label_id=2,
            labels=labels,
            tickets=tickets,
            members=members,
            projects=projects,
        )

# TC18: projectsがNone
def test_attach_label_form_projects_none_TC18():
    labels = Mock()
    labels.attach = Mock()
    tickets = Mock()
    members = Mock()
    projects = None
    request = DummyRequest()
    with pytest.raises(AttributeError):
        attach_label_form(
            ticket_id=1,
            request=request,
            label_id=2,
            labels=labels,
            tickets=tickets,
            members=members,
            projects=projects,
        )