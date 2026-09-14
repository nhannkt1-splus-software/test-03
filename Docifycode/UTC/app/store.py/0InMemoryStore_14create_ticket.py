import pytest

# --- 必要なダミークラス・Enum・関数の定義 ---
from enum import Enum, auto
from datetime import datetime, timedelta

# Priority Enumのダミー実装
class Priority(Enum):
    HIGH = auto()
    NORMAL = auto()
    LOW = auto()

# Ticketクラスのダミー実装
class Ticket:
    def __init__(self, id, title, description, priority, assignee, project_id):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.assignee = assignee
        self.project_id = project_id
        self.created_at = datetime.now()
        self.due_at = None

# due_at_for関数のダミー実装
def due_at_for(created_at, priority):
    if not isinstance(priority, Priority):
        raise TypeError("priority must be Priority")
    if priority == Priority.HIGH:
        return created_at + timedelta(days=1)
    elif priority == Priority.NORMAL:
        return created_at + timedelta(days=3)
    elif priority == Priority.LOW:
        return created_at + timedelta(days=7)
    else:
        raise ValueError("Invalid priority value")

# InMemoryStoreのテスト用インポート
from types import SimpleNamespace

# --- テスト対象クラスのインポート ---
# ここでは問題文のクラスをそのまま利用
# from your_module import InMemoryStore

# テスト用InMemoryStoreのダミー実装
class InMemoryStore:
    """Process-local store. Enough for dummy CRUD and unit tests."""

    def __init__(self):
        self._next_ticket_id = 1
        self.tickets = {}

    def create_ticket(
        self,
        title: str,
        description: str,
        priority: Priority,
        assignee: str | None,
        project_id: int | None = None,
    ) -> Ticket:
        ticket = Ticket(
            id=self._next_ticket_id,
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            project_id=project_id,
        )
        ticket.due_at = due_at_for(ticket.created_at, ticket.priority)
        self.tickets[ticket.id] = ticket
        self._next_ticket_id += 1
        return ticket

# --- テスト本体 ---

# 長い文字列生成用
LONG_TITLE = "a" * 1000
LONG_DESCRIPTION = "b" * 5000

# Priorityの不正値用ダミー
class FakePriority(Enum):
    INVALID = auto()

# --- テストケース ---

# TC1: 正常系：全ての入力が有効な値
def test_create_ticket_TC1():
    # TC1
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=1,
    )
    # 期待値の検証
    assert isinstance(ticket, Ticket)
    assert ticket.title == "正常なタイトル"
    assert ticket.description == "正常な説明"
    assert ticket.priority == Priority.HIGH
    assert ticket.assignee == "assignee_user"
    assert ticket.project_id == 1

# TC2: 正常系：タイトルが空文字列
def test_create_ticket_TC2():
    # TC2
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="",
        description="正常な説明",
        priority=Priority.NORMAL,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.title == ""

# TC3: 正常系：タイトルが非常に長い文字列
def test_create_ticket_TC3():
    # TC3
    store = InMemoryStore()
    ticket = store.create_ticket(
        title=LONG_TITLE,
        description="正常な説明",
        priority=Priority.LOW,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.title == LONG_TITLE

# TC4: 異常系：タイトルがint型（型不一致）
def test_create_ticket_TC4():
    # TC4
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title=123,
            description="正常な説明",
            priority=Priority.HIGH,
            assignee="assignee_user",
            project_id=1,
        )

# TC5: 異常系：タイトルがNone
def test_create_ticket_TC5():
    # TC5
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title=None,
            description="正常な説明",
            priority=Priority.HIGH,
            assignee="assignee_user",
            project_id=1,
        )

# TC6: 正常系：説明が空文字列
def test_create_ticket_TC6():
    # TC6
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.description == ""

# TC7: 正常系：説明が非常に長い文字列
def test_create_ticket_TC7():
    # TC7
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description=LONG_DESCRIPTION,
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.description == LONG_DESCRIPTION

# TC8: 異常系：説明がNone
def test_create_ticket_TC8():
    # TC8
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title="正常なタイトル",
            description=None,
            priority=Priority.HIGH,
            assignee="assignee_user",
            project_id=1,
        )

# TC9: 異常系：priorityがstr型（型不一致）
def test_create_ticket_TC9():
    # TC9
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority="HIGH",
            assignee="assignee_user",
            project_id=1,
        )

# TC10: 異常系：priorityがNone
def test_create_ticket_TC10():
    # TC10
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=None,
            assignee="assignee_user",
            project_id=1,
        )

# TC11: 正常系：assigneeが空文字列
def test_create_ticket_TC11():
    # TC11
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee="",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.assignee == ""

# TC12: 正常系：assigneeがNone
def test_create_ticket_TC12():
    # TC12
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee=None,
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.assignee is None

# TC13: 異常系：assigneeがint型（型不一致）
def test_create_ticket_TC13():
    # TC13
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.HIGH,
            assignee=123,
            project_id=1,
        )

# TC14: 正常系：project_idが0（境界値）
def test_create_ticket_TC14():
    # TC14
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=0,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id == 0

# TC15: 正常系：project_idが負の値（異常値だが許容される場合）
def test_create_ticket_TC15():
    # TC15
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=-1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id == -1

# TC16: 正常系：project_idがNone
def test_create_ticket_TC16():
    # TC16
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=None,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id is None

# TC17: 異常系：project_idがstr型（型不一致）
def test_create_ticket_TC17():
    # TC17
    store = InMemoryStore()
    with pytest.raises(TypeError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.HIGH,
            assignee="assignee_user",
            project_id="project1",
        )

# TC18: 異常系：self._next_ticket_idやself.ticketsが未初期化の場合
def test_create_ticket_TC18():
    # TC18
    store = InMemoryStore()
    # 属性を削除して未初期化状態を再現
    del store._next_ticket_id
    del store.tickets
    with pytest.raises(AttributeError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.HIGH,
            assignee="assignee_user",
            project_id=1,
        )

# TC19: 異常系：priorityがPriority型だが不正値（due_at_forでValueError発生）
def test_create_ticket_TC19():
    # TC19
    store = InMemoryStore()
    # FakePriority.INVALIDはPriority型ではないが、型チェックを通すためにcast
    class BadPriority(Priority):
        INVALID = 99
    bad_priority = FakePriority.INVALID
    # ただし、due_at_forでValueErrorを発生させるため、Priority型の未知値を渡す
    # ここではEnumの継承でなく、Priorityの値として未知値を直接渡す
    # ただし、due_at_forの実装によってはTypeErrorになる場合もある
    class DummyPriority(Priority):
        INVALID = 99
    with pytest.raises(ValueError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=DummyPriority.INVALID,
            assignee="assignee_user",
            project_id=1,
        )

# TC20: 正常系：assigneeとproject_idが両方None
def test_create_ticket_TC20():
    # TC20
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.LOW,
        assignee=None,
        project_id=None,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.assignee is None
    assert ticket.project_id is None

# TC21: 正常系：project_idがNone（priorityがNORMAL）
def test_create_ticket_TC21():
    # TC21
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.NORMAL,
        assignee="assignee_user",
        project_id=None,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id is None

# TC22: 正常系：project_idが負の値（LOW優先度）
def test_create_ticket_TC22():
    # TC22
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.LOW,
        assignee="assignee_user",
        project_id=-1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id == -1

# TC23: 正常系：project_idがNone（HIGH優先度）
def test_create_ticket_TC23():
    # TC23
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.HIGH,
        assignee="assignee_user",
        project_id=None,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id is None

# TC24: 正常系：assigneeが空文字列（NORMAL優先度）
def test_create_ticket_TC24():
    # TC24
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.NORMAL,
        assignee="",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.assignee == ""

# TC25: 正常系：project_idが0（LOW優先度）
def test_create_ticket_TC25():
    # TC25
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="正常な説明",
        priority=Priority.LOW,
        assignee="assignee_user",
        project_id=0,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.project_id == 0

# TC26: 正常系：descriptionが空文字列（NORMAL優先度）
def test_create_ticket_TC26():
    # TC26
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description="",
        priority=Priority.NORMAL,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.description == ""

# TC27: 正常系：descriptionが非常に長い文字列（NORMAL優先度）
def test_create_ticket_TC27():
    # TC27
    store = InMemoryStore()
    ticket = store.create_ticket(
        title="正常なタイトル",
        description=LONG_DESCRIPTION,
        priority=Priority.NORMAL,
        assignee="assignee_user",
        project_id=1,
    )
    assert isinstance(ticket, Ticket)
    assert ticket.description == LONG_DESCRIPTION

# TC28: 異常系：self.ticketsがNoneの場合
def test_create_ticket_TC28():
    # TC28
    store = InMemoryStore()
    store.tickets = None
    with pytest.raises(TypeError):
        store.create_ticket(
            title="正常なタイトル",
            description="正常な説明",
            priority=Priority.HIGH,
            assignee="assignee_user",
            project_id=1,
        )