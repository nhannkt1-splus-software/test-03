import pytest
from unittest.mock import MagicMock, patch

# --- テスト用ダミー定義 ---
import types

# Priority, Ticketのダミー定義
class Priority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Ticket:
    def __init__(self, title, description, priority, assignee, project_id):
        self.title = title
        self.description = description
        self.priority = priority
        self.assignee = assignee
        self.project_id = project_id

# TicketServiceのダミー依存関数をパッチするfixture
@pytest.fixture
def ticket_service():
    from target_module import TicketService  # テスト対象のモジュール名に合わせて修正
    service = TicketService()
    # _resolve_assignee, _resolve_project_idはそのまま値を返すようにモック
    service._resolve_assignee = MagicMock(side_effect=lambda x: x)
    service._resolve_project_id = MagicMock(side_effect=lambda x: x)
    # store.create_ticketは正常時はTicketを返す
    service.store = MagicMock()
    service.store.create_ticket = MagicMock(
        side_effect=lambda **kwargs: Ticket(**kwargs)
    )
    return service

# store.create_ticketでValueErrorを発生させるfixture
@pytest.fixture
def ticket_service_valueerror():
    from target_module import TicketService  # テスト対象のモジュール名に合わせて修正
    service = TicketService()
    service._resolve_assignee = MagicMock(side_effect=lambda x: x)
    service._resolve_project_id = MagicMock(side_effect=lambda x: x)
    service.store = MagicMock()
    service.store.create_ticket = MagicMock(side_effect=ValueError("Invalid project_id"))
    return service

# --- 各テストケース ---

# TC1: 正常系：全ての入力が有効な値
def test_create_ticket_tc1(ticket_service):
    # TC1
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.MEDIUM,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(result, Ticket)
    assert result.title == "正常なタイトル"
    assert result.description == "正常な説明"
    assert result.priority == Priority.MEDIUM
    assert result.assignee == "assignee_user"
    assert result.project_id == 1

# TC2: title, descriptionに前後空白がある場合のstrip動作確認
def test_create_ticket_tc2(ticket_service):
    # TC2
    result = ticket_service.create_ticket(
        title="   前後に空白があるタイトル   ",
        description="   前後に空白がある説明   ",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=1,
    )
    assert result.title == "前後に空白があるタイトル"
    assert result.description == "前後に空白がある説明"
    assert result.priority == Priority.HIGH

# TC3: title, descriptionが空文字列の場合
def test_create_ticket_tc3(ticket_service):
    # TC3
    result = ticket_service.create_ticket(
        title="",
        description="",
        priority=Priority.LOW,
        assignee="assignee_user",
        project_id=1,
    )
    assert result.title == ""
    assert result.description == ""
    assert result.priority == Priority.LOW

# TC4: assignee未指定（None）の場合
def test_create_ticket_tc4(ticket_service):
    # TC4
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.MEDIUM,
        assignee=None,
        project_id=1,
    )
    assert result.assignee is None

# TC5: project_id未指定（None）の場合
def test_create_ticket_tc5(ticket_service):
    # TC5
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.MEDIUM,
        assignee="assignee_user",
        project_id=None,
    )
    assert result.project_id is None

# TC6: titleがint型で型不一致
def test_create_ticket_tc6(ticket_service):
    # TC6
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title=123,
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=1,
        )

# TC7: titleがNoneTypeで型不一致
def test_create_ticket_tc7(ticket_service):
    # TC7
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title=None,
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=1,
        )

# TC8: descriptionがint型で型不一致
def test_create_ticket_tc8(ticket_service):
    # TC8
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description=123,
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=1,
        )

# TC9: descriptionがNoneTypeで型不一致
def test_create_ticket_tc9(ticket_service):
    # TC9
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description=None,
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=1,
        )

# TC10: priorityがstr型で型不一致
def test_create_ticket_tc10(ticket_service):
    # TC10
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority="HIGH",
            assignee="assignee_user",
            project_id=1,
        )

# TC11: priorityがNoneTypeで型不一致
def test_create_ticket_tc11(ticket_service):
    # TC11
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=None,
            assignee="assignee_user",
            project_id=1,
        )

# TC12: assigneeがint型で型不一致
def test_create_ticket_tc12(ticket_service):
    # TC12
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee=123,
            project_id=1,
        )

# TC13: assigneeがlist型で型不一致
def test_create_ticket_tc13(ticket_service):
    # TC13
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee=[],
            project_id=1,
        )

# TC14: assigneeが空文字列の場合
def test_create_ticket_tc14(ticket_service):
    # TC14
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.MEDIUM,
        assignee="",
        project_id=1,
    )
    assert result.assignee == ""

# TC15: project_idがstr型で型不一致
def test_create_ticket_tc15(ticket_service):
    # TC15
    with pytest.raises(TypeError):
        ticket_service.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id="1",
        )

# TC16: project_idが-1（存在しないID、store側で例外発生）
def test_create_ticket_tc16(ticket_service_valueerror):
    # TC16
    with pytest.raises(ValueError):
        ticket_service_valueerror.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=-1,
        )

# TC17: project_idが0（存在しないID、store側で例外発生）
def test_create_ticket_tc17(ticket_service_valueerror):
    # TC17
    with pytest.raises(ValueError):
        ticket_service_valueerror.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=0,
        )

# TC18: assigneeとproject_idが両方Noneの場合
def test_create_ticket_tc18(ticket_service):
    # TC18
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee=None,
        project_id=None,
    )
    assert result.assignee is None
    assert result.project_id is None

# TC19: assigneeが空文字列、project_idがNoneの場合
def test_create_ticket_tc19(ticket_service):
    # TC19
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.LOW,
        assignee="",
        project_id=None,
    )
    assert result.assignee == ""
    assert result.project_id is None

# TC20: project_idのみNoneの場合
def test_create_ticket_tc20(ticket_service):
    # TC20
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.MEDIUM,
        assignee="assignee_user",
        project_id=None,
    )
    assert result.project_id is None

# TC21: assigneeのみNoneの場合
def test_create_ticket_tc21(ticket_service):
    # TC21
    result = ticket_service.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.MEDIUM,
        assignee=None,
        project_id=1,
    )
    assert result.assignee is None

# TC22: project_idが-1（存在しないID、store側で例外発生）
def test_create_ticket_tc22(ticket_service_valueerror):
    # TC22
    with pytest.raises(ValueError):
        ticket_service_valueerror.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=-1,
        )

# TC23: project_idが0（存在しないID、store側で例外発生）
def test_create_ticket_tc23(ticket_service_valueerror):
    # TC23
    with pytest.raises(ValueError):
        ticket_service_valueerror.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.MEDIUM,
            assignee="assignee_user",
            project_id=0,
        )