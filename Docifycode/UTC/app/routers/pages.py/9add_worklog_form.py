import pytest
from unittest.mock import Mock, create_autospec
from fastapi import Request
from starlette.responses import RedirectResponse

# --- テスト用のダミークラス・例外定義 ---
class DeskError(Exception):
    pass

# _ticket_errorは異常系で呼ばれるため、モック化する
import sys

# テスト対象関数のimport
from importlib import import_module

# テスト対象関数のあるモジュール名（例: app.main など）
# ここでは 'target_module' と仮定
target_module = import_module("target_module")
add_worklog_form = target_module.add_worklog_form

# _ticket_errorをpatchするためにimport
_ticket_error = target_module._ticket_error

# --- 共通のモック生成関数 ---
def make_request():
    # FastAPIのRequestのモック
    req = create_autospec(Request, instance=True)
    return req

def make_service_mock():
    return Mock()

# --- テストケース ---

# TC1: 正常系：全ての入力が有効な場合
def test_TC1():
    # テストID: TC1
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    # add_worklogは正常
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    # 303リダイレクトが返ること
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC2: 境界値テスト：ticket_idが0の場合
def test_TC2():
    # テストID: TC2
    ticket_id = 0
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC3: ticket_idが負数でDeskError発生
def test_TC3(monkeypatch):
    # テストID: TC3
    ticket_id = -1
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    worklogs.add_worklog.side_effect = DeskError("invalid ticket_id")
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    # _ticket_errorが呼ばれることを確認
    called = {}
    def fake_ticket_error(request_, ticket_id_, msg, tickets_, members_, projects_, labels_):
        called["called"] = True
        return "error"
    monkeypatch.setattr(target_module, "_ticket_error", fake_ticket_error)
    result = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert result == "error"
    assert called["called"]

# TC4: ticket_idがstr型（型不一致）
def test_TC4():
    # テストID: TC4
    ticket_id = "abc"
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(TypeError):
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )

# TC5: 非常に大きいticket_id
def test_TC5():
    # テストID: TC5
    ticket_id = 1000000000
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC6: ticket_idがfloat型（型不一致）
def test_TC6():
    # テストID: TC6
    ticket_id = 0.5
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(TypeError):
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )

# TC7: hoursが0.0
def test_TC7():
    # テストID: TC7
    ticket_id = 1
    hours = 0.0
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC8: hoursが負数でDeskError発生
def test_TC8(monkeypatch):
    # テストID: TC8
    ticket_id = 1
    hours = -2.0
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    worklogs.add_worklog.side_effect = DeskError("negative hours")
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    def fake_ticket_error(request_, ticket_id_, msg, tickets_, members_, projects_, labels_):
        return "error"
    monkeypatch.setattr(target_module, "_ticket_error", fake_ticket_error)
    result = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert result == "error"

# TC9: hoursがstr型（型不一致）
def test_TC9():
    # テストID: TC9
    ticket_id = 1
    hours = "2"
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(TypeError):
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )

# TC10: hoursがNone（未入力）
def test_TC10():
    # テストID: TC10
    ticket_id = 1
    hours = None
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(ValueError):
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )

# TC11: authorが空文字列でDeskError発生
def test_TC11(monkeypatch):
    # テストID: TC11
    ticket_id = 1
    hours = 1.5
    author = ""
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    worklogs.add_worklog.side_effect = DeskError("empty author")
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    def fake_ticket_error(request_, ticket_id_, msg, tickets_, members_, projects_, labels_):
        return "error"
    monkeypatch.setattr(target_module, "_ticket_error", fake_ticket_error)
    result = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert result == "error"

# TC12: authorがNone（未入力）
def test_TC12():
    # テストID: TC12
    ticket_id = 1
    hours = 1.5
    author = None
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(ValueError):
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )

# TC13: authorがint型（型不一致）
def test_TC13():
    # テストID: TC13
    ticket_id = 1
    hours = 1.5
    author = 123
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(TypeError):
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )

# TC14: noteが空文字列（デフォルト値）
def test_TC14():
    # テストID: TC14
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = ""
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC15: noteがNone
def test_TC15():
    # テストID: TC15
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = None
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC16: add_worklogでDeskError発生
def test_TC16(monkeypatch):
    # テストID: TC16
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    worklogs.add_worklog.side_effect = DeskError("error")
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    def fake_ticket_error(request_, ticket_id_, msg, tickets_, members_, projects_, labels_):
        return "error"
    monkeypatch.setattr(target_module, "_ticket_error", fake_ticket_error)
    result = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert result == "error"

# TC17: add_worklogでDeskError以外の例外発生時（未捕捉例外）
def test_TC17():
    # テストID: TC17
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    worklogs.add_worklog.side_effect = Exception("unexpected error")
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    with pytest.raises(Exception) as excinfo:
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )
    assert "unexpected error" in str(excinfo.value)

# TC18: noteが非常に長い文字列
def test_TC18():
    # テストID: TC18
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = "a" * 1000
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    response = add_worklog_form(
        ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC19: _ticket_error内で例外発生
def test_TC19(monkeypatch):
    # テストID: TC19
    ticket_id = 1
    hours = 1.5
    author = "user1"
    note = "作業内容"
    request = make_request()
    worklogs = make_service_mock()
    tickets = make_service_mock()
    members = make_service_mock()
    projects = make_service_mock()
    labels = make_service_mock()
    # add_worklogは正常
    # _ticket_errorで例外
    def fake_ticket_error(request_, ticket_id_, msg, tickets_, members_, projects_, labels_):
        raise Exception("error in _ticket_error")
    monkeypatch.setattr(target_module, "_ticket_error", fake_ticket_error)
    # worklogs.add_worklogはDeskErrorを発生させることで_ticket_errorに流す
    worklogs.add_worklog.side_effect = DeskError("error")
    with pytest.raises(Exception) as excinfo:
        add_worklog_form(
            ticket_id, request, hours, author, note, worklogs, tickets, members, projects, labels
        )
    assert "error in _ticket_error" in str(excinfo.value)
```
