import pytest
from unittest.mock import Mock
from fastapi import Request
from starlette.responses import RedirectResponse

# --- テスト用のダミークラスと例外定義 ---
class DeskError(Exception):
    pass

# assign_form関数のimport
from target_module import assign_form  # ← assign_formの定義ファイル名に合わせて修正してください

# --- テスト用のダミーサービス ---
@pytest.fixture
def mock_label_service():
    return Mock()

@pytest.fixture
def mock_member_service():
    return Mock()

@pytest.fixture
def mock_project_service():
    return Mock()

@pytest.fixture
def mock_ticket_service():
    return Mock()

@pytest.fixture
def mock_request():
    return Mock(spec=Request)

# --- _ticket_errorのモック ---
@pytest.fixture(autouse=True)
def patch_ticket_error(monkeypatch):
    # _ticket_errorの戻り値をモック
    monkeypatch.setattr("target_module._ticket_error", lambda *args, **kwargs: "ticket_error_response")

# --- assign_formのテスト ---
# TC1: tickets.assignが正常終了
def test_assign_form_tc1(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    # tickets.assignが正常終了
    mock_ticket_service.assign.return_value = None
    # username: 有効なユーザー名
    username = "valid_user"
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # リダイレクトレスポンスが返ること
    # TC1
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC2: tickets.assignがDeskError例外を送出
def test_assign_form_tc2(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    # tickets.assignがDeskError例外
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = "valid_user"
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # _ticket_errorの戻り値が返ること
    # TC2
    assert response == "ticket_error_response"

# TC3: tickets.assignがDeskError例外を送出（ticket_id=0）
def test_assign_form_tc3(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = "valid_user"
    ticket_id = 0
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC3
    assert response == "ticket_error_response"

# TC4: tickets.assignがDeskError例外を送出（ticket_id=-1）
def test_assign_form_tc4(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = "valid_user"
    ticket_id = -1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC4
    assert response == "ticket_error_response"

# TC5: ticket_idが文字列（型不一致）
def test_assign_form_tc5(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    username = "valid_user"
    ticket_id = "abc"
    # TypeErrorが発生すること
    # TC5
    with pytest.raises(TypeError):
        assign_form(
            ticket_id=ticket_id,
            request=mock_request,
            username=username,
            tickets=mock_ticket_service,
            members=mock_member_service,
            projects=mock_project_service,
            labels=mock_label_service,
        )

# TC6: ticket_idがNone（型不一致）
def test_assign_form_tc6(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    username = "valid_user"
    ticket_id = None
    # TypeErrorが発生すること
    # TC6
    with pytest.raises(TypeError):
        assign_form(
            ticket_id=ticket_id,
            request=mock_request,
            username=username,
            tickets=mock_ticket_service,
            members=mock_member_service,
            projects=mock_project_service,
            labels=mock_label_service,
        )

# TC7: usernameが空文字（正常系）
def test_assign_form_tc7(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.return_value = None
    username = ""
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC7
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"
    # assignの引数がNoneになること
    mock_ticket_service.assign.assert_called_with(ticket_id, None)

# TC8: usernameがNone（型不一致）
def test_assign_form_tc8(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    username = None
    ticket_id = 1
    # TypeErrorが発生すること
    # TC8
    with pytest.raises(TypeError):
        assign_form(
            ticket_id=ticket_id,
            request=mock_request,
            username=username,
            tickets=mock_ticket_service,
            members=mock_member_service,
            projects=mock_project_service,
            labels=mock_label_service,
        )

# TC9: usernameが整数（型不一致）
def test_assign_form_tc9(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    username = 123
    ticket_id = 1
    # TypeErrorが発生すること
    # TC9
    with pytest.raises(TypeError):
        assign_form(
            ticket_id=ticket_id,
            request=mock_request,
            username=username,
            tickets=mock_ticket_service,
            members=mock_member_service,
            projects=mock_project_service,
            labels=mock_label_service,
        )

# TC10: 依存サービスが正常な場合
def test_assign_form_tc10(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.return_value = None
    username = "valid_user"
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC10
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC11: 依存サービス（tickets）が例外を送出
def test_assign_form_tc11(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = "valid_user"
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC11
    assert response == "ticket_error_response"

# TC12: ticket_id=0, username=""でassignがDeskError例外
def test_assign_form_tc12(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = ""
    ticket_id = 0
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC12
    assert response == "ticket_error_response"

# TC13: ticket_id=-1, username=""でassignがDeskError例外
def test_assign_form_tc13(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = ""
    ticket_id = -1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC13
    assert response == "ticket_error_response"

# TC14: usernameが空文字でassignがDeskError例外
def test_assign_form_tc14(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.side_effect = DeskError("error")
    username = ""
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC14
    assert response == "ticket_error_response"

# TC15: ticket_id=0でassignが正常終了
def test_assign_form_tc15(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.return_value = None
    username = "valid_user"
    ticket_id = 0
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC15
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC16: ticket_id=-1でassignが正常終了
def test_assign_form_tc16(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.return_value = None
    username = "valid_user"
    ticket_id = -1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC16
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"

# TC17: usernameが空文字でassignが正常終了
def test_assign_form_tc17(mock_ticket_service, mock_label_service, mock_member_service, mock_project_service, mock_request):
    mock_ticket_service.assign.return_value = None
    username = ""
    ticket_id = 1
    response = assign_form(
        ticket_id=ticket_id,
        request=mock_request,
        username=username,
        tickets=mock_ticket_service,
        members=mock_member_service,
        projects=mock_project_service,
        labels=mock_label_service,
    )
    # TC17
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == f"/tickets/{ticket_id}"
    mock_ticket_service.assign.assert_called_with(ticket_id, None)
```
