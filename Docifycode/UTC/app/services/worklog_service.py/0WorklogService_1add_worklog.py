import pytest

# --- テスト用ダミー定数・クラス定義 ---
MAX_WORKLOG_HOURS = 8.0
MAX_TICKET_HOURS = 40.0

class InvalidWorklogError(Exception):
    def __init__(self, hours):
        self.hours = hours

class WorklogLimitError(Exception):
    def __init__(self, ticket_id, total, max_hours):
        self.ticket_id = ticket_id
        self.total = total
        self.max_hours = max_hours

class TicketNotWritableError(Exception):
    pass

class WorklogAddError(Exception):
    pass

class Worklog:
    def __init__(self, hours, author, note):
        self.hours = hours
        self.author = author
        self.note = note

class Ticket:
    def __init__(self, ticket_id, writable=True, logged_hours=0.0):
        self.id = ticket_id
        self.writable = writable
        self.logged_hours = logged_hours
        self.add_worklog_called = False
        self.raise_add_worklog = False

    def add_worklog(self, hours, author, note):
        self.add_worklog_called = True
        if self.raise_add_worklog:
            raise WorklogAddError()
        return Worklog(hours, author, note)

# --- テスト用ダミーサービス ---
class WorklogService:
    def __init__(self):
        # テスト用チケットデータ
        self.tickets = {
            1: Ticket(1, writable=True, logged_hours=0.0),
            2: Ticket(2, writable=False, logged_hours=0.0),
        }
        self.raise_add_worklog = False
        self.logged_hours_override = {}

    def _get_writable_ticket(self, ticket_id):
        # ticket_id型チェック
        if not isinstance(ticket_id, int):
            raise TypeError()
        if ticket_id is None or ticket_id < 0:
            raise TicketNotWritableError()
        if ticket_id not in self.tickets:
            raise TicketNotWritableError()
        ticket = self.tickets[ticket_id]
        if not ticket.writable:
            raise TicketNotWritableError()
        return ticket

    def add_worklog(
        self,
        ticket_id: int,
        hours: float,
        author: str,
        note: str = "",
    ) -> Worklog:
        # 型チェック
        if not isinstance(ticket_id, int):
            raise TypeError()
        if not isinstance(hours, float):
            raise TypeError()
        if not isinstance(author, str):
            raise TypeError()
        if not isinstance(note, str):
            raise TypeError()
        ticket = self._get_writable_ticket(ticket_id)
        if hours <= 0 or hours > MAX_WORKLOG_HOURS:
            raise InvalidWorklogError(hours)
        # hours_loggedのオーバーライド
        total = self.logged_hours_override.get(ticket_id, ticket.logged_hours) + hours
        if total > MAX_TICKET_HOURS:
            raise WorklogLimitError(ticket.id, total, MAX_TICKET_HOURS)
        ticket.raise_add_worklog = self.raise_add_worklog
        return ticket.add_worklog(hours, author.strip(), note.strip())

# --- テストケース ---
@pytest.fixture
def service():
    return WorklogService()

# TC1: 正常系：全ての入力が正常な場合
def test_TC1(service):
    # TC1
    result = service.add_worklog(1, 1.0, "user", "note")
    assert isinstance(result, Worklog)
    assert result.hours == 1.0
    assert result.author == "user"
    assert result.note == "note"

# TC2: hoursが上限値（MAX_WORKLOG_HOURS）の場合
def test_TC2(service):
    # TC2
    result = service.add_worklog(1, MAX_WORKLOG_HOURS, "user", "note")
    assert isinstance(result, Worklog)
    assert result.hours == MAX_WORKLOG_HOURS

# TC3: hoursが最小の正の値（境界値）
def test_TC3(service):
    # TC3
    result = service.add_worklog(1, 0.1, "user", "note")
    assert isinstance(result, Worklog)
    assert result.hours == 0.1

# TC4: hoursが0の場合
def test_TC4(service):
    # TC4
    with pytest.raises(InvalidWorklogError):
        service.add_worklog(1, 0.0, "user", "note")

# TC5: hoursが負の値の場合
def test_TC5(service):
    # TC5
    with pytest.raises(InvalidWorklogError):
        service.add_worklog(1, -1.0, "user", "note")

# TC6: hoursがMAX_WORKLOG_HOURS超過
def test_TC6(service):
    # TC6
    with pytest.raises(InvalidWorklogError):
        service.add_worklog(1, MAX_WORKLOG_HOURS + 0.1, "user", "note")

# TC7: hours_logged(ticket) + hoursがMAX_TICKET_HOURSを超える場合
def test_TC7(service):
    # TC7
    service.logged_hours_override[1] = MAX_TICKET_HOURS - 1.0
    with pytest.raises(WorklogLimitError):
        service.add_worklog(1, 100.0, "user", "note")

# TC8: 存在しないチケットID
def test_TC8(service):
    # TC8
    with pytest.raises(TicketNotWritableError):
        service.add_worklog(0, 1.0, "user", "note")

# TC9: ticket_idが負の値
def test_TC9(service):
    # TC9
    with pytest.raises(TicketNotWritableError):
        service.add_worklog(-1, 1.0, "user", "note")

# TC10: 書き込み不可チケットID
def test_TC10(service):
    # TC10
    with pytest.raises(TicketNotWritableError):
        service.add_worklog(2, 1.0, "user", "note")

# TC11: ticket_idがstr型
def test_TC11(service):
    # TC11
    with pytest.raises(TypeError):
        service.add_worklog("1", 1.0, "user", "note")

# TC12: ticket_idがNone
def test_TC12(service):
    # TC12
    with pytest.raises(TypeError):
        service.add_worklog(None, 1.0, "user", "note")

# TC13: hoursがstr型
def test_TC13(service):
    # TC13
    with pytest.raises(TypeError):
        service.add_worklog(1, "2", "user", "note")

# TC14: hoursがNone
def test_TC14(service):
    # TC14
    with pytest.raises(TypeError):
        service.add_worklog(1, None, "user", "note")

# TC15: authorがNone
def test_TC15(service):
    # TC15
    with pytest.raises(TypeError):
        service.add_worklog(1, 1.0, None, "note")

# TC16: authorがint型
def test_TC16(service):
    # TC16
    with pytest.raises(TypeError):
        service.add_worklog(1, 1.0, 123, "note")

# TC17: authorが空文字
def test_TC17(service):
    # TC17
    result = service.add_worklog(1, 1.0, "", "note")
    assert isinstance(result, Worklog)
    assert result.author == ""

# TC18: authorに前後空白あり（stripされることの確認）
def test_TC18(service):
    # TC18
    result = service.add_worklog(1, 1.0, " user ", "note")
    assert isinstance(result, Worklog)
    assert result.author == "user"

# TC19: noteがNone
def test_TC19(service):
    # TC19
    with pytest.raises(TypeError):
        service.add_worklog(1, 1.0, "user", None)

# TC20: noteがint型
def test_TC20(service):
    # TC20
    with pytest.raises(TypeError):
        service.add_worklog(1, 1.0, "user", 123)

# TC21: noteが空文字
def test_TC21(service):
    # TC21
    result = service.add_worklog(1, 1.0, "user", "")
    assert isinstance(result, Worklog)
    assert result.note == ""

# TC22: noteに前後空白あり（stripされることの確認）
def test_TC22(service):
    # TC22
    result = service.add_worklog(1, 1.0, "user", " note ")
    assert isinstance(result, Worklog)
    assert result.note == "note"

# TC23: ticket.add_worklogで例外発生
def test_TC23(service):
    # TC23
    service.raise_add_worklog = True
    with pytest.raises(WorklogAddError):
        service.add_worklog(1, 1.0, "user", "note")

# TC24: noteが非常に長い文字列の場合
def test_TC24(service):
    # TC24
    long_note = "a" * 1000
    result = service.add_worklog(1, 1.0, "user", long_note)
    assert isinstance(result, Worklog)
    assert result.note == long_note

# TC25: authorが非常に長い文字列の場合
def test_TC25(service):
    # TC25
    long_author = "a" * 1000
    result = service.add_worklog(1, 1.0, long_author, "note")
    assert isinstance(result, Worklog)
    assert result.author == long_author