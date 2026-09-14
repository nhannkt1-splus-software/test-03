import pytest
from datetime import datetime, timedelta

# --- テスト用ダミー定義 ---
# Priority列挙型のダミー
class Priority:
    HIGH = "high"
    LOW = "low"
    INVALID = "invalid"

# Ticketクラスのダミー
class Ticket:
    def __init__(self, ticket_id, title, description, priority, assignee, created_at, due_at, updated_at, closed=False):
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.priority = priority
        self.assignee = assignee
        self.created_at = created_at
        self.due_at = due_at
        self.updated_at = updated_at
        self.closed = closed

# due_at_for関数のダミー
def due_at_for(created_at, priority):
    if priority == Priority.HIGH:
        return created_at + timedelta(days=1)
    elif priority == Priority.LOW:
        return created_at + timedelta(days=7)
    elif priority == Priority.INVALID:
        raise Exception("Invalid priority")
    else:
        return created_at + timedelta(days=3)

# utc_now関数のダミー
def utc_now():
    return datetime.utcnow()

# --- TicketServiceのテスト用サブクラス ---
class TicketServiceTestable(TicketService):
    def __init__(self):
        # チケットDBのダミー
        self.tickets = {
            1: Ticket(1, "元タイトル", "元説明", Priority.LOW, "user1", datetime(2024, 6, 1), due_at_for(datetime(2024, 6, 1), Priority.LOW), datetime(2024, 6, 1)),
            2: Ticket(2, "閉じたタイトル", "閉じた説明", Priority.HIGH, "user1", datetime(2024, 6, 1), due_at_for(datetime(2024, 6, 1), Priority.HIGH), datetime(2024, 6, 1), closed=True),
        }
        self.valid_users = {"user1", "user2"}

    def get_ticket(self, ticket_id):
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        ticket = self.tickets.get(ticket_id)
        if ticket is None:
            raise Exception("Ticket not found")
        return ticket

    def _ensure_not_closed(self, ticket, action):
        if getattr(ticket, "closed", False):
            raise Exception("Ticket is closed")

    def _resolve_assignee(self, assignee):
        if not isinstance(assignee, str):
            raise TypeError("assignee must be str")
        resolved = assignee.strip()
        if resolved not in self.valid_users:
            raise Exception("Assignee not found")
        return resolved

# --- テストケース ---
@pytest.fixture
def service():
    return TicketServiceTestable()

@pytest.fixture
def fresh_ticket(service):
    # チケットID1を毎回リセット
    service.tickets[1] = Ticket(1, "元タイトル", "元説明", Priority.LOW, "user1", datetime(2024, 6, 1), due_at_for(datetime(2024, 6, 1), Priority.LOW), datetime(2024, 6, 1))
    return service.tickets[1]

# TC1: 全てのパラメータが有効な値で指定された場合
def test_TC1_update_all_fields(service, fresh_ticket):
    # TC1
    result = service.update_ticket(
        ticket_id=1,
        title="新しいタイトル",
        description="新しい説明",
        priority=Priority.HIGH,
        assignee="user1"
    )
    assert result.title == "新しいタイトル"
    assert result.description == "新しい説明"
    assert result.priority == Priority.HIGH
    assert result.assignee == "user1"
    assert result.due_at == due_at_for(result.created_at, Priority.HIGH)
    assert result.updated_at > result.created_at

# TC2: 全ての更新項目がNoneの場合（何も変更されない）
def test_TC2_update_none(service, fresh_ticket):
    # TC2
    before = fresh_ticket
    result = service.update_ticket(
        ticket_id=1,
        title=None,
        description=None,
        priority=None,
        assignee=None
    )
    assert result.title == before.title
    assert result.description == before.description
    assert result.priority == before.priority
    assert result.assignee == before.assignee
    assert result.due_at == before.due_at

# TC3: title, descriptionの前後空白が除去されて更新される
def test_TC3_strip_title_description(service, fresh_ticket):
    # TC3
    result = service.update_ticket(
        ticket_id=1,
        title="   タイトル前後に空白   ",
        description="   説明前後に空白   ",
        priority=None,
        assignee=None
    )
    assert result.title == "タイトル前後に空白"
    assert result.description == "説明前後に空白"

# TC4: title, descriptionが空文字で更新されるケース
def test_TC4_empty_title_description(service, fresh_ticket):
    # TC4
    result = service.update_ticket(
        ticket_id=1,
        title="",
        description="",
        priority=None,
        assignee=None
    )
    assert result.title == ""
    assert result.description == ""

# TC5: priorityのみ更新し、due_atも更新される
def test_TC5_update_priority(service, fresh_ticket):
    # TC5
    result = service.update_ticket(
        ticket_id=1,
        title=None,
        description=None,
        priority=Priority.LOW,
        assignee=None
    )
    assert result.priority == Priority.LOW
    assert result.due_at == due_at_for(result.created_at, Priority.LOW)

# TC6: assigneeの前後空白が除去されてユーザー解決される
def test_TC6_strip_assignee(service, fresh_ticket):
    # TC6
    result = service.update_ticket(
        ticket_id=1,
        title=None,
        description=None,
        priority=None,
        assignee="   user2   "
    )
    assert result.assignee == "user2"

# TC7: 存在しないチケットIDを指定した場合
def test_TC7_ticket_not_found(service):
    # TC7
    with pytest.raises(Exception) as e:
        service.update_ticket(
            ticket_id=99999,
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.HIGH,
            assignee="user1"
        )
    assert str(e.value) == "Ticket not found"

# TC8: 閉じているチケットを更新しようとした場合
def test_TC8_closed_ticket(service):
    # TC8
    with pytest.raises(Exception) as e:
        service.update_ticket(
            ticket_id=2,
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.HIGH,
            assignee="user1"
        )
    assert str(e.value) == "Ticket is closed"

# TC9: 無効なPriority値を指定した場合
def test_TC9_invalid_priority(service, fresh_ticket):
    # TC9
    with pytest.raises(Exception) as e:
        service.update_ticket(
            ticket_id=1,
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.INVALID,
            assignee="user1"
        )
    assert str(e.value) == "Invalid priority"

# TC10: 存在しないユーザー名をassigneeに指定した場合
def test_TC10_assignee_not_found(service, fresh_ticket):
    # TC10
    with pytest.raises(Exception) as e:
        service.update_ticket(
            ticket_id=1,
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.HIGH,
            assignee="unknown_user"
        )
    assert str(e.value) == "Assignee not found"

# TC11: ticket_idがNoneの場合（型不一致）
def test_TC11_ticket_id_none(service):
    # TC11
    with pytest.raises(TypeError):
        service.update_ticket(
            ticket_id=None,
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.HIGH,
            assignee="user1"
        )

# TC12: ticket_idがstr型の場合（型不一致）
def test_TC12_ticket_id_str(service):
    # TC12
    with pytest.raises(TypeError):
        service.update_ticket(
            ticket_id="abc",
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.HIGH,
            assignee="user1"
        )

# TC13: titleがint型の場合（型不一致）
def test_TC13_title_int(service, fresh_ticket):
    # TC13
    with pytest.raises(TypeError):
        service.update_ticket(
            ticket_id=1,
            title=123,
            description="新しい説明",
            priority=Priority.HIGH,
            assignee="user1"
        )

# TC14: descriptionがint型の場合（型不一致）
def test_TC14_description_int(service, fresh_ticket):
    # TC14
    with pytest.raises(TypeError):
        service.update_ticket(
            ticket_id=1,
            title="新しいタイトル",
            description=123,
            priority=Priority.HIGH,
            assignee="user1"
        )

# TC15: priorityがstr型の場合（型不一致）
def test_TC15_priority_str(service, fresh_ticket):
    # TC15
    with pytest.raises(TypeError):
        service.update_ticket(
            ticket_id=1,
            title="新しいタイトル",
            description="新しい説明",
            priority="high",
            assignee="user1"
        )

# TC16: assigneeがint型の場合（型不一致）
def test_TC16_assignee_int(service, fresh_ticket):
    # TC16
    with pytest.raises(TypeError):
        service.update_ticket(
            ticket_id=1,
            title="新しいタイトル",
            description="新しい説明",
            priority=Priority.HIGH,
            assignee=123
        )

# TC17: assigneeに存在しないユーザー名を指定した場合（priority未指定）
def test_TC17_assignee_not_found_no_priority(service, fresh_ticket):
    # TC17
    with pytest.raises(Exception) as e:
        service.update_ticket(
            ticket_id=1,
            title="新しいタイトル",
            description="新しい説明",
            priority=None,
            assignee="unknown_user"
        )
    assert str(e.value) == "Assignee not found"

# TC18: priorityに無効な値を指定し、他は未指定の場合
def test_TC18_invalid_priority_only(service, fresh_ticket):
    # TC18
    with pytest.raises(Exception) as e:
        service.update_ticket(
            ticket_id=1,
            title=None,
            description=None,
            priority=Priority.INVALID,
            assignee=None
        )
    assert str(e.value) == "Invalid priority"

# TC19: assignee未指定でtitle, description, priorityのみ更新
def test_TC19_update_title_description_priority(service, fresh_ticket):
    # TC19
    result = service.update_ticket(
        ticket_id=1,
        title="新しいタイトル",
        description="新しい説明",
        priority=Priority.HIGH,
        assignee=None
    )
    assert result.title == "新しいタイトル"
    assert result.description == "新しい説明"
    assert result.priority == Priority.HIGH
    assert result.assignee == "user1"
    assert result.due_at == due_at_for(result.created_at, Priority.HIGH)

# TC20: descriptionのみ更新されるケース
def test_TC20_update_description_only(service, fresh_ticket):
    # TC20
    result = service.update_ticket(
        ticket_id=1,
        title=None,
        description="新しい説明",
        priority=None,
        assignee=None
    )
    assert result.description == "新しい説明"
    assert result.title == "元タイトル"

# TC21: titleのみ更新されるケース
def test_TC21_update_title_only(service, fresh_ticket):
    # TC21
    result = service.update_ticket(
        ticket_id=1,
        title="新しいタイトル",
        description=None,
        priority=None,
        assignee=None
    )
    assert result.title == "新しいタイトル"
    assert result.description == "元説明"