import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from pydantic import ValidationError

# --- 必要なクラス・関数のimport ---
# テスト対象の関数
from your_module import create_ticket

# テストで使う型
from your_module import TicketCreate, TicketOut, DeskError, to_ticket_out

# --- ヘルパー: テスト用のTicketインスタンスを作成 ---
class DummyTicket:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def make_ticket(**kwargs):
    # 必要なフィールドを適宜追加
    return DummyTicket(**kwargs)

# --- ヘルパー: serviceのMockを作成 ---
def make_service(create_ticket_return=None, create_ticket_side_effect=None):
    service = Mock()
    if create_ticket_side_effect is not None:
        service.create_ticket.side_effect = create_ticket_side_effect
    else:
        service.create_ticket.return_value = create_ticket_return
    return service

# --- TC19-26用: DeskError→HTTPException変換のためのhttp_errorモック ---
@pytest.fixture(autouse=True)
def patch_http_error():
    with patch("your_module.http_error", side_effect=lambda exc: HTTPException(status_code=400, detail=str(exc))):
        yield

# --- TC1: 正常系：全てのフィールドが正しい値 ---
def test_create_ticket_tc1():
    # TC1
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    ticket = make_ticket(id=1, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        # to_ticket_outが呼ばれ、戻り値が返ること
        assert result == "ticket_out"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC2: titleが空文字列 ---
def test_create_ticket_tc2():
    # TC2
    payload = TicketCreate(
        title="",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    ticket = make_ticket(id=2, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out2") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        assert result == "ticket_out2"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC3: descriptionが空文字列 ---
def test_create_ticket_tc3():
    # TC3
    payload = TicketCreate(
        title="valid title",
        description="",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    ticket = make_ticket(id=3, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out3") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        assert result == "ticket_out3"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC4: priorityが最小値（0） ---
def test_create_ticket_tc4():
    # TC4
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=0,
        assignee="user1",
        project_id=100,
    )
    ticket = make_ticket(id=4, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out4") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        assert result == "ticket_out4"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC5: priorityが最大値（5） ---
def test_create_ticket_tc5():
    # TC5
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=5,
        assignee="user1",
        project_id=100,
    )
    ticket = make_ticket(id=5, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out5") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        assert result == "ticket_out5"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC6: priorityが負の値（-1） ---
def test_create_ticket_tc6():
    # TC6
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority=-1,
            assignee="user1",
            project_id=100,
        )

# --- TC7: priorityが文字列型 ---
def test_create_ticket_tc7():
    # TC7
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority="high",  # 不正な型
            assignee="user1",
            project_id=100,
        )

# --- TC8: assigneeが空文字列 ---
def test_create_ticket_tc8():
    # TC8
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="",
        project_id=100,
    )
    ticket = make_ticket(id=8, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out8") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        assert result == "ticket_out8"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC9: project_idが0 ---
def test_create_ticket_tc9():
    # TC9
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=0,
    )
    ticket = make_ticket(id=9, title=payload.title, description=payload.description, priority=payload.priority, assignee=payload.assignee, project_id=payload.project_id)
    service = make_service(create_ticket_return=ticket)
    with patch("your_module.to_ticket_out", return_value="ticket_out9") as mock_to_ticket_out:
        result = create_ticket(payload, service)
        assert result == "ticket_out9"
        mock_to_ticket_out.assert_called_once_with(ticket)

# --- TC10: project_idが負の値（-1） ---
def test_create_ticket_tc10():
    # TC10
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority=1,
            assignee="user1",
            project_id=-1,
        )

# --- TC11: project_idが文字列型 ---
def test_create_ticket_tc11():
    # TC11
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority=1,
            assignee="user1",
            project_id="abc",  # 不正な型
        )

# --- TC12: titleがnull ---
def test_create_ticket_tc12():
    # TC12
    with pytest.raises(ValidationError):
        TicketCreate(
            title=None,
            description="valid description",
            priority=1,
            assignee="user1",
            project_id=100,
        )

# --- TC13: descriptionがnull ---
def test_create_ticket_tc13():
    # TC13
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description=None,
            priority=1,
            assignee="user1",
            project_id=100,
        )

# --- TC14: priorityがnull ---
def test_create_ticket_tc14():
    # TC14
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority=None,
            assignee="user1",
            project_id=100,
        )

# --- TC15: assigneeがnull ---
def test_create_ticket_tc15():
    # TC15
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority=1,
            assignee=None,
            project_id=100,
        )

# --- TC16: project_idがnull ---
def test_create_ticket_tc16():
    # TC16
    with pytest.raises(ValidationError):
        TicketCreate(
            title="valid title",
            description="valid description",
            priority=1,
            assignee="user1",
            project_id=None,
        )

# --- TC17: 全てのフィールドが欠落しているケース ---
def test_create_ticket_tc17():
    # TC17
    with pytest.raises(ValidationError):
        TicketCreate(**{})

# --- TC18: payloadがNoneの場合 ---
def test_create_ticket_tc18():
    # TC18
    service = make_service(create_ticket_return=None)
    with pytest.raises(TypeError):
        create_ticket(None, service)

# --- TC19: service.create_ticketでDeskError例外発生（正常な入力値） ---
def test_create_ticket_tc19():
    # TC19
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error19"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error19" in str(excinfo.value.detail)

# --- TC20: service.create_ticketでDeskError例外発生（正常な入力値） ---
def test_create_ticket_tc20():
    # TC20
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error20"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error20" in str(excinfo.value.detail)

# --- TC21: titleが空文字列でservice.create_ticketがDeskError例外を返すケース ---
def test_create_ticket_tc21():
    # TC21
    payload = TicketCreate(
        title="",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error21"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error21" in str(excinfo.value.detail)

# --- TC22: descriptionが空文字列でservice.create_ticketがDeskError例外を返すケース ---
def test_create_ticket_tc22():
    # TC22
    payload = TicketCreate(
        title="valid title",
        description="",
        priority=1,
        assignee="user1",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error22"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error22" in str(excinfo.value.detail)

# --- TC23: priorityが最小値（0）でservice.create_ticketがDeskError例外を返すケース ---
def test_create_ticket_tc23():
    # TC23
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=0,
        assignee="user1",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error23"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error23" in str(excinfo.value.detail)

# --- TC24: priorityが最大値（5）でservice.create_ticketがDeskError例外を返すケース ---
def test_create_ticket_tc24():
    # TC24
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=5,
        assignee="user1",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error24"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error24" in str(excinfo.value.detail)

# --- TC25: assigneeが空文字列でservice.create_ticketがDeskError例外を返すケース ---
def test_create_ticket_tc25():
    # TC25
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="",
        project_id=100,
    )
    service = make_service(create_ticket_side_effect=DeskError("error25"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error25" in str(excinfo.value.detail)

# --- TC26: project_idが0でservice.create_ticketがDeskError例外を返すケース ---
def test_create_ticket_tc26():
    # TC26
    payload = TicketCreate(
        title="valid title",
        description="valid description",
        priority=1,
        assignee="user1",
        project_id=0,
    )
    service = make_service(create_ticket_side_effect=DeskError("error26"))
    with pytest.raises(HTTPException) as excinfo:
        create_ticket(payload, service)
    assert "error26" in str(excinfo.value.detail)