import pytest
from datetime import datetime, timedelta
from types import SimpleNamespace
import math

# --- 必要なクラス・関数のモック定義 ---
# 本来はimportで読み込むが、テスト用に最低限の定義を行う
import sys

# TicketStatus, Priority, Comment, Worklog, utc_nowが未定義の場合はモックする
try:
    TicketStatus
except NameError:
    from enum import Enum, auto
    class TicketStatus(Enum):
        OPEN = auto()
        CLOSED = auto()
    class Priority(Enum):
        LOW = auto()
        MEDIUM = auto()
        HIGH = auto()
    class Comment:
        pass
    class Worklog:
        def __init__(self, id, hours, author, note):
            self.id = id
            self.hours = hours
            self.author = author
            self.note = note
        def __eq__(self, other):
            return (
                isinstance(other, Worklog) and
                self.id == other.id and
                (
                    (math.isnan(self.hours) and math.isnan(other.hours))
                    if isinstance(self.hours, float) and isinstance(other.hours, float) and math.isnan(self.hours)
                    else self.hours == other.hours
                ) and
                self.author == other.author and
                self.note == other.note
            )
        def __repr__(self):
            return f"Worklog(id={self.id}, hours={self.hours}, author={self.author!r}, note={self.note!r})"
    def utc_now():
        return datetime.utcnow()

from dataclasses import dataclass, field

# --- Ticketクラスのimportまたは再定義 ---
# 本来はimportで読み込むが、テスト用に最低限の定義を行う
try:
    Ticket
except NameError:
    @dataclass
    class Ticket:
        id: int = 1
        title: str = ""
        description: str = ""
        status: TicketStatus = TicketStatus.OPEN
        priority: Priority = Priority.MEDIUM
        assignee: str | None = None
        project_id: int | None = None
        label_ids: list[int] = field(default_factory=list)
        comments: list[Comment] = field(default_factory=list)
        worklogs: list[Worklog] = field(default_factory=list)
        due_at: datetime | None = None
        created_at: datetime = field(default_factory=utc_now)
        updated_at: datetime = field(default_factory=utc_now)
        _next_comment_id: int = field(default=1, repr=False)
        _next_worklog_id: int = field(default=1, repr=False)
        def add_worklog(self, hours: float, author: str, note: str = "") -> Worklog:
            worklog = Worklog(
                id=self._next_worklog_id,
                hours=hours,
                author=author,
                note=note,
            )
            self._next_worklog_id += 1
            self.worklogs.append(worklog)
            self.updated_at = utc_now()
            return worklog

# --- utc_nowのパッチ用ヘルパ ---
import builtins

# --- テストケース ---

# TC1: 正常系: 標準的な入力
def test_add_worklog_TC1():
    # TC1
    ticket = Ticket()
    result = ticket.add_worklog(1.0, "user1")
    assert result == Worklog(id=1, hours=1.0, author="user1", note="")
    assert ticket.worklogs[-1] == result

# TC2: 境界値: 作業時間が0
def test_add_worklog_TC2():
    # TC2
    ticket = Ticket()
    result = ticket.add_worklog(0.0, "user1")
    assert result == Worklog(id=1, hours=0.0, author="user1", note="")
    assert ticket.worklogs[-1] == result

# TC3: 異常系: 負の作業時間（現状は例外にならないが、仕様上要検討）
def test_add_worklog_TC3():
    # TC3
    ticket = Ticket()
    result = ticket.add_worklog(-1.0, "user1")
    assert result == Worklog(id=1, hours=-1.0, author="user1", note="")
    assert ticket.worklogs[-1] == result

# TC4: 境界値: 非常に大きい作業時間
def test_add_worklog_TC4():
    # TC4
    ticket = Ticket()
    result = ticket.add_worklog(10000.0, "user1")
    assert result == Worklog(id=1, hours=10000.0, author="user1", note="")
    assert ticket.worklogs[-1] == result

# TC5: 正常系: noteに文字列
def test_add_worklog_TC5():
    # TC5
    ticket = Ticket()
    result = ticket.add_worklog(1.5, "user1", "長いメモ")
    assert result == Worklog(id=1, hours=1.5, author="user1", note="長いメモ")
    assert ticket.worklogs[-1] == result

# TC6: 異常系: authorが空文字列（現状は例外にならないが、仕様上要検討）
def test_add_worklog_TC6():
    # TC6
    ticket = Ticket()
    result = ticket.add_worklog(1.0, "")
    assert result == Worklog(id=1, hours=1.0, author="", note="")
    assert ticket.worklogs[-1] == result

# TC7: 異常系: authorがNone
def test_add_worklog_TC7():
    # TC7
    ticket = Ticket()
    with pytest.raises(TypeError):
        ticket.add_worklog(1.0, None)

# TC8: 異常系: hoursがstr型
def test_add_worklog_TC8():
    # TC8
    ticket = Ticket()
    with pytest.raises(TypeError):
        ticket.add_worklog("1.0", "user1")

# TC9: 異常系: authorがint型
def test_add_worklog_TC9():
    # TC9
    ticket = Ticket()
    with pytest.raises(TypeError):
        ticket.add_worklog(1.0, 123)

# TC10: 異常系: noteがNone
def test_add_worklog_TC10():
    # TC10
    ticket = Ticket()
    with pytest.raises(TypeError):
        ticket.add_worklog(1.0, "user1", None)

# TC11: 異常系: noteがint型
def test_add_worklog_TC11():
    # TC11
    ticket = Ticket()
    with pytest.raises(TypeError):
        ticket.add_worklog(1.0, "user1", 123)

# TC12: 正常系: noteが非常に長い文字列
def test_add_worklog_TC12():
    # TC12
    ticket = Ticket()
    long_note = "a" * 1000
    result = ticket.add_worklog(1.0, "user1", long_note)
    assert result == Worklog(id=1, hours=1.0, author="user1", note=long_note)
    assert ticket.worklogs[-1] == result

# TC13: 異常系: utc_now()が例外を投げる場合
def test_add_worklog_TC13(monkeypatch):
    # TC13
    ticket = Ticket()
    def raise_exc():
        raise Exception("utc_now error")
    monkeypatch.setattr(sys.modules[ticket.__class__.__module__], "utc_now", raise_exc)
    with pytest.raises(Exception) as e:
        ticket.add_worklog(1.0, "user1")
    assert "utc_now error" in str(e.value)

# TC14: 異常系: hoursがNaN（現状は例外にならないが、仕様上要検討）
def test_add_worklog_TC14():
    # TC14
    ticket = Ticket()
    nan_val = float('nan')
    result = ticket.add_worklog(nan_val, "user1")
    assert math.isnan(result.hours)
    assert result.author == "user1"
    assert result.note == ""
    assert ticket.worklogs[-1] == result

# TC15: 異常系: hoursがInfinity（現状は例外にならないが、仕様上要検討）
def test_add_worklog_TC15():
    # TC15
    ticket = Ticket()
    inf_val = float('inf')
    result = ticket.add_worklog(inf_val, "user1")
    assert math.isinf(result.hours)
    assert result.author == "user1"
    assert result.note == ""
    assert ticket.worklogs[-1] == result

# TC16: 異常系: utc_now()が未来の日時を返す場合（現状は例外にならないが、仕様上要検討）
def test_add_worklog_TC16(monkeypatch):
    # TC16
    ticket = Ticket()
    future_time = datetime.utcnow() + timedelta(days=365)
    monkeypatch.setattr(sys.modules[ticket.__class__.__module__], "utc_now", lambda: future_time)
    result = ticket.add_worklog(1.0, "user1")
    assert result == Worklog(id=1, hours=1.0, author="user1", note="")
    assert ticket.updated_at == future_time
    assert ticket.worklogs[-1] == result
```
