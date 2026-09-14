import pytest
from collections import Counter
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

# --- テスト用ダミーEnumと出力クラス定義 ---
import enum

class TicketStatus(enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    UNKNOWN = "UNKNOWN"

class BoardStatsOut:
    def __init__(self, total_tickets, by_status, overdue, hours_logged, active_members, open_projects):
        self.total_tickets = total_tickets
        self.by_status = by_status
        self.overdue = overdue
        self.hours_logged = hours_logged
        self.active_members = active_members
        self.open_projects = open_projects

    def __eq__(self, other):
        if not isinstance(other, BoardStatsOut):
            return False
        return (
            self.total_tickets == other.total_tickets and
            self.by_status == other.by_status and
            self.overdue == other.overdue and
            self.hours_logged == other.hours_logged and
            self.active_members == other.active_members and
            self.open_projects == other.open_projects
        )

# --- テスト対象クラスのimport ---
from types import SimpleNamespace

# テスト対象のStatsServiceをimportまたは定義
# from your_module import StatsService

# --- テスト用ヘルパー ---
def make_ticket(status, hours=None):
    t = SimpleNamespace()
    t.status = status
    t._hours = hours
    return t

def make_member(active):
    m = SimpleNamespace()
    m.active = active
    return m

def make_project(archived):
    p = SimpleNamespace()
    p.archived = archived
    return p

# --- テスト本体 ---
@pytest.fixture(autouse=True)
def patch_enums_and_output(monkeypatch):
    # StatsServiceの中で使われるTicketStatus, BoardStatsOutをpatch
    import sys
    import builtins
    # BoardStatsOut
    monkeypatch.setitem(globals(), "BoardStatsOut", BoardStatsOut)
    # TicketStatus
    monkeypatch.setitem(globals(), "TicketStatus", TicketStatus)
    yield

# --- 各テストケース ---

# TC1: 全て空リストの場合の正常系
def test_TC1(monkeypatch):
    # チケット・メンバー・プロジェクト全て空
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[])
    store.list_members = MagicMock(return_value=[])
    store.list_projects = MagicMock(return_value=[])

    # is_overdue, hours_loggedは呼ばれない
    monkeypatch.setitem(globals(), "is_overdue", MagicMock())
    monkeypatch.setitem(globals(), "hours_logged", MagicMock())

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=0,
        by_status={s.value: 0 for s in TicketStatus},
        overdue=0,
        hours_logged=0.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC2: チケットが1件のみ、overdueでなくhours_loggedが1.5の正常系
def test_TC2(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    store.list_members = MagicMock(return_value=[])
    store.list_projects = MagicMock(return_value=[])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.5))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=1.5,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC3: 複数件のチケット、overdueやhours_loggedが混在する正常系
def test_TC3(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    ticket2 = make_ticket(TicketStatus.IN_PROGRESS)
    ticket3 = make_ticket(TicketStatus.DONE)
    tickets = [ticket1, ticket2, ticket3]
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=tickets)
    member1 = make_member(True)
    member2 = make_member(True)
    store.list_members = MagicMock(return_value=[member1, member2])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    # is_overdue: ticket1=False, ticket2=True, ticket3=False
    def is_overdue_side_effect(ticket):
        if ticket is ticket1:
            return False
        elif ticket is ticket2:
            return True
        elif ticket is ticket3:
            return False
    monkeypatch.setitem(globals(), "is_overdue", MagicMock(side_effect=is_overdue_side_effect))

    # hours_logged: ticket1=1.0, ticket2=2.25, ticket3=0.5
    def hours_logged_side_effect(ticket):
        if ticket is ticket1:
            return 1.0
        elif ticket is ticket2:
            return 2.25
        elif ticket is ticket3:
            return 0.5
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(side_effect=hours_logged_side_effect))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=3,
        by_status={
            TicketStatus.OPEN.value: 1,
            TicketStatus.IN_PROGRESS.value: 1,
            TicketStatus.DONE.value: 1,
            TicketStatus.UNKNOWN.value: 0
        },
        overdue=1,
        hours_logged=round(1.0 + 2.25 + 0.5, 2),
        active_members=2,
        open_projects=1
    )
    result = svc.summarize()
    assert result == expected

# TC4: 全て同じstatusのチケットのみの場合
def test_TC4(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    ticket2 = make_ticket(TicketStatus.OPEN)
    tickets = [ticket1, ticket2]
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=tickets)
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(True)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=2,
        by_status={s.value: 2 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=2.0,
        active_members=1,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC5: 全て異なるstatusのチケットのみの場合
def test_TC5(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    ticket2 = make_ticket(TicketStatus.IN_PROGRESS)
    ticket3 = make_ticket(TicketStatus.DONE)
    tickets = [ticket1, ticket2, ticket3]
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=tickets)
    store.list_members = MagicMock(return_value=[])
    project1 = make_project(False)
    project2 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1, project2])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=3,
        by_status={
            TicketStatus.OPEN.value: 1,
            TicketStatus.IN_PROGRESS.value: 1,
            TicketStatus.DONE.value: 1,
            TicketStatus.UNKNOWN.value: 0
        },
        overdue=0,
        hours_logged=3.0,
        active_members=0,
        open_projects=2
    )
    result = svc.summarize()
    assert result == expected

# TC6: statusが未定義値のチケットのみの場合
def test_TC6(monkeypatch):
    ticket1 = make_ticket(TicketStatus.UNKNOWN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    store.list_members = MagicMock(return_value=[])
    store.list_projects = MagicMock(return_value=[])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=0.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.UNKNOWN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=0.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC7: list_all()がNoneを返す異常系
def test_TC7(monkeypatch):
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=None)
    store.list_members = MagicMock(return_value=[])
    store.list_projects = MagicMock(return_value=[])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock())
    monkeypatch.setitem(globals(), "hours_logged", MagicMock())

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()

# TC8: list_all()がTypeErrorを投げる異常系
def test_TC8(monkeypatch):
    store = SimpleNamespace()
    store.list_all = MagicMock(side_effect=TypeError)
    store.list_members = MagicMock(return_value=[])
    store.list_projects = MagicMock(return_value=[])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock())
    monkeypatch.setitem(globals(), "hours_logged", MagicMock())

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()

# TC9: overdue=Trueのチケットのみ、activeメンバー・openプロジェクトなし
def test_TC9(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(False)
    member2 = make_member(False)
    store.list_members = MagicMock(return_value=[member1, member2])
    project1 = make_project(True)
    project2 = make_project(True)
    store.list_projects = MagicMock(return_value=[project1, project2])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=True))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=0.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=1,
        hours_logged=0.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC10: hours_loggedが負の値のケース
def test_TC10(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=-2.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=-2.0,
        active_members=1,
        open_projects=1
    )
    result = svc.summarize()
    assert result == expected

# TC11: hours_loggedが小数点以下2桁以上のケース（四捨五入）
def test_TC11(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.2345))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=1.23,
        active_members=1,
        open_projects=1
    )
    result = svc.summarize()
    assert result == expected

# TC12: activeメンバー・openプロジェクトが0のケース
def test_TC12(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(False)
    member2 = make_member(False)
    store.list_members = MagicMock(return_value=[member1, member2])
    project1 = make_project(True)
    project2 = make_project(True)
    store.list_projects = MagicMock(return_value=[project1, project2])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=0.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=0.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC13: activeメンバー・openプロジェクトが複数のケース
def test_TC13(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    member2 = make_member(True)
    store.list_members = MagicMock(return_value=[member1, member2])
    project1 = make_project(False)
    project2 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1, project2])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=1.0,
        active_members=2,
        open_projects=2
    )
    result = svc.summarize()
    assert result == expected

# TC14: プロジェクトが空リストのケース
def test_TC14(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    store.list_projects = MagicMock(return_value=[])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=1.0,
        active_members=1,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC15: 全てarchived=Trueのプロジェクトのみ
def test_TC15(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    store.list_members = MagicMock(return_value=[])
    project1 = make_project(True)
    project2 = make_project(True)
    store.list_projects = MagicMock(return_value=[project1, project2])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=1.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC16: 全てarchived=Falseのプロジェクトのみ
def test_TC16(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    store.list_members = MagicMock(return_value=[])
    project1 = make_project(False)
    project2 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1, project2])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=1,
        by_status={s.value: 1 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=1.0,
        active_members=0,
        open_projects=2
    )
    result = svc.summarize()
    assert result == expected

# TC17: is_overdueが例外を投げる異常系
def test_TC17(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    def is_overdue_raise(ticket):
        raise Exception("is_overdue error")
    monkeypatch.setitem(globals(), "is_overdue", is_overdue_raise)
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(Exception):
        svc.summarize()

# TC18: hours_loggedが例外を投げる異常系
def test_TC18(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    def hours_logged_raise(ticket):
        raise Exception("hours_logged error")
    monkeypatch.setitem(globals(), "hours_logged", hours_logged_raise)

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(Exception):
        svc.summarize()

# TC19: チケットのstatus属性が存在しない異常系
def test_TC19(monkeypatch):
    ticket1 = SimpleNamespace()  # status属性なし
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(AttributeError):
        svc.summarize()

# TC20: メンバーのactive属性が存在しない異常系
def test_TC20(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = SimpleNamespace()  # active属性なし
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(AttributeError):
        svc.summarize()

# TC21: プロジェクトのarchived属性が存在しない異常系
def test_TC21(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = SimpleNamespace()  # archived属性なし
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(AttributeError):
        svc.summarize()

# TC22: 複数チケットでoverdueが混在し、hours_loggedが全て0のケース
def test_TC22(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    ticket2 = make_ticket(TicketStatus.IN_PROGRESS)
    tickets = [ticket1, ticket2]
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=tickets)
    store.list_members = MagicMock(return_value=[])
    store.list_projects = MagicMock(return_value=[])

    def is_overdue_side_effect(ticket):
        if ticket is ticket1:
            return True
        elif ticket is ticket2:
            return False
    monkeypatch.setitem(globals(), "is_overdue", MagicMock(side_effect=is_overdue_side_effect))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=0.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=2,
        by_status={
            TicketStatus.OPEN.value: 1,
            TicketStatus.IN_PROGRESS.value: 1,
            TicketStatus.DONE.value: 0,
            TicketStatus.UNKNOWN.value: 0
        },
        overdue=1,
        hours_logged=0.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC23: 全て同じstatus、hours_loggedが0、activeメンバー・openプロジェクトなしのケース
def test_TC23(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    ticket2 = make_ticket(TicketStatus.OPEN)
    ticket3 = make_ticket(TicketStatus.OPEN)
    tickets = [ticket1, ticket2, ticket3]
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=tickets)
    member1 = make_member(False)
    member2 = make_member(False)
    member3 = make_member(False)
    store.list_members = MagicMock(return_value=[member1, member2, member3])
    project1 = make_project(True)
    project2 = make_project(True)
    project3 = make_project(True)
    store.list_projects = MagicMock(return_value=[project1, project2, project3])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=0.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    expected = BoardStatsOut(
        total_tickets=3,
        by_status={s.value: 3 if s == TicketStatus.OPEN else 0 for s in TicketStatus},
        overdue=0,
        hours_logged=0.0,
        active_members=0,
        open_projects=0
    )
    result = svc.summarize()
    assert result == expected

# TC24: hours_loggedが小数点以下2桁以上の複数チケット（四捨五入合計）のケース
def test_TC24(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    ticket2 = make_ticket(TicketStatus.IN_PROGRESS)
    ticket3 = make_ticket(TicketStatus.DONE)
    tickets = [ticket1, ticket2, ticket3]
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=tickets)
    member1 = make_member(True)
    member2 = make_member(False)
    store.list_members = MagicMock(return_value=[member1, member2])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    def hours_logged_side_effect(ticket):
        if ticket is ticket1:
            return 0.12345
        elif ticket is ticket2:
            return 0.6789
        elif ticket is ticket3:
            return 0.9999
    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(side_effect=hours_logged_side_effect))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    total = round(0.12345 + 0.6789 + 0.9999, 2)
    expected = BoardStatsOut(
        total_tickets=3,
        by_status={
            TicketStatus.OPEN.value: 1,
            TicketStatus.IN_PROGRESS.value: 1,
            TicketStatus.DONE.value: 1,
            TicketStatus.UNKNOWN.value: 0
        },
        overdue=0,
        hours_logged=total,
        active_members=1,
        open_projects=1
    )
    result = svc.summarize()
    assert result == expected

# TC25: list_members()がTypeErrorを投げる異常系
def test_TC25(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    store.list_members = MagicMock(side_effect=TypeError)
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()

# TC26: list_projects()がTypeErrorを投げる異常系
def test_TC26(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    store.list_projects = MagicMock(side_effect=TypeError)

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()

# TC27: hours_loggedがNoneを返す異常系
def test_TC27(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=None))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()

# TC28: メンバーのactive属性がNoneの場合の異常系
def test_TC28(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(None)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(False)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()

# TC29: プロジェクトのarchived属性がNoneの場合の異常系
def test_TC29(monkeypatch):
    ticket1 = make_ticket(TicketStatus.OPEN)
    store = SimpleNamespace()
    store.list_all = MagicMock(return_value=[ticket1])
    member1 = make_member(True)
    store.list_members = MagicMock(return_value=[member1])
    project1 = make_project(None)
    store.list_projects = MagicMock(return_value=[project1])

    monkeypatch.setitem(globals(), "is_overdue", MagicMock(return_value=False))
    monkeypatch.setitem(globals(), "hours_logged", MagicMock(return_value=1.0))

    from your_module import StatsService
    svc = StatsService()
    svc.store = store

    with pytest.raises(TypeError):
        svc.summarize()