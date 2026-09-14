import pytest

# テスト対象関数の依存型や例外型をモックする
class DeskError(Exception):
    pass

class HTTPException(Exception):
    pass

def http_error(exc):
    # DeskErrorをHTTPExceptionに変換するモック
    return HTTPException(str(exc))

# TicketUpdate, TicketOut, TicketService, to_ticket_outをモック
class TicketUpdate:
    def __init__(self, title, description, priority, assignee):
        self.title = title
        self.description = description
        self.priority = priority
        self.assignee = assignee

class TicketOut:
    def __init__(self, ticket):
        self.ticket = ticket

def to_ticket_out(ticket):
    return TicketOut(ticket)

class TicketService:
    def update_ticket(self, ticket_id, title, description, priority, assignee):
        # テストケースごとにモックの振る舞いを切り替えるため、pytestのfixtureで差し替える
        pass

def get_ticket_service():
    return TicketService()

# テスト対象関数をimportまたは直接定義（ここでは直接定義）
def update_ticket(
    ticket_id,
    payload,
    service=None,
):
    if service is None:
        service = get_ticket_service()
    try:
        ticket = service.update_ticket(
            ticket_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            assignee=payload.assignee,
        )
        return to_ticket_out(ticket)
    except DeskError as exc:
        raise http_error(exc) from exc

# 各テストケースのパターンをfixtureで管理
@pytest.fixture
def mock_service(monkeypatch):
    class MockService(TicketService):
        def update_ticket(self, ticket_id, title, description, priority, assignee):
            # デフォルトは正常系
            return {
                "ticket_id": ticket_id,
                "title": title,
                "description": description,
                "priority": priority,
                "assignee": assignee,
            }
    return MockService()

@pytest.fixture
def mock_service_deskerror(monkeypatch):
    class MockService(TicketService):
        def update_ticket(self, ticket_id, title, description, priority, assignee):
            raise DeskError("desk error")
    return MockService()

@pytest.fixture
def mock_service_deskerror_notfound(monkeypatch):
    class MockService(TicketService):
        def update_ticket(self, ticket_id, title, description, priority, assignee):
            raise DeskError("not found")
    return MockService()

@pytest.fixture
def mock_service_deskerror_permission(monkeypatch):
    class MockService(TicketService):
        def update_ticket(self, ticket_id, title, description, priority, assignee):
            raise DeskError("permission error")
    return MockService()

@pytest.fixture
def mock_service_valueerror(monkeypatch):
    class MockService(TicketService):
        def update_ticket(self, ticket_id, title, description, priority, assignee):
            raise ValueError("invalid value")
    return MockService()

# --- テストケース ---
# TC1: 正常系：全ての値が正しい場合
def test_update_ticket_tc1(mock_service):
    # TC1
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    result = update_ticket(1, payload, service=mock_service)
    # 期待値: TicketOutインスタンス
    assert isinstance(result, TicketOut)
    assert result.ticket["ticket_id"] == 1
    assert result.ticket["title"] == "新しいタイトル"
    assert result.ticket["description"] == "新しい説明"
    assert result.ticket["priority"] == 1
    assert result.ticket["assignee"] == "user1"

# TC2: ticket_id=0（存在しないチケットID）
def test_update_ticket_tc2(mock_service_deskerror):
    # TC2
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(0, payload, service=mock_service_deskerror)

# TC3: ticket_id=-1（負のチケットID）
def test_update_ticket_tc3(mock_service_deskerror):
    # TC3
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(-1, payload, service=mock_service_deskerror)

# TC4: ticket_id=999999（非常に大きいチケットID）
def test_update_ticket_tc4(mock_service_deskerror):
    # TC4
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(999999, payload, service=mock_service_deskerror)

# TC5: ticket_id="abc"（型不一致：文字列）
def test_update_ticket_tc5(mock_service):
    # TC5
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(TypeError):
        update_ticket("abc", payload, service=mock_service)

# TC6: ticket_id=None
def test_update_ticket_tc6(mock_service):
    # TC6
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(TypeError):
        update_ticket(None, payload, service=mock_service)

# TC7: title/descriptionが空文字
def test_update_ticket_tc7(mock_service):
    # TC7
    payload = TicketUpdate("", "", 1, "user1")
    result = update_ticket(1, payload, service=mock_service)
    assert isinstance(result, TicketOut)
    assert result.ticket["title"] == ""
    assert result.ticket["description"] == ""

# TC8: priorityが境界値（0）
def test_update_ticket_tc8(mock_service):
    # TC8
    payload = TicketUpdate("新しいタイトル", "新しい説明", 0, "user1")
    result = update_ticket(1, payload, service=mock_service)
    assert isinstance(result, TicketOut)
    assert result.ticket["priority"] == 0

# TC9: priorityが負の値
def test_update_ticket_tc9(mock_service_valueerror):
    # TC9
    payload = TicketUpdate("新しいタイトル", "新しい説明", -1, "user1")
    with pytest.raises(ValueError):
        update_ticket(1, payload, service=mock_service_valueerror)

# TC10: priorityが非常に大きい値（許容範囲内と仮定）
def test_update_ticket_tc10(mock_service):
    # TC10
    payload = TicketUpdate("新しいタイトル", "新しい説明", 999, "user1")
    result = update_ticket(1, payload, service=mock_service)
    assert isinstance(result, TicketOut)
    assert result.ticket["priority"] == 999

# TC11: priorityが型不一致（文字列）
def test_update_ticket_tc11(mock_service):
    # TC11
    payload = TicketUpdate("新しいタイトル", "新しい説明", "high", "user1")
    with pytest.raises(TypeError):
        update_ticket(1, payload, service=mock_service)

# TC12: assigneeがNone
def test_update_ticket_tc12(mock_service):
    # TC12
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, None)
    result = update_ticket(1, payload, service=mock_service)
    assert isinstance(result, TicketOut)
    assert result.ticket["assignee"] is None

# TC13: payloadの全項目がNone
def test_update_ticket_tc13(mock_service_valueerror):
    # TC13
    payload = TicketUpdate(None, None, None, None)
    with pytest.raises(ValueError):
        update_ticket(1, payload, service=mock_service_valueerror)

# TC14: payloadがNone
def test_update_ticket_tc14(mock_service):
    # TC14
    with pytest.raises(TypeError):
        update_ticket(1, None, service=mock_service)

# TC15: payloadがリスト（型不一致）
def test_update_ticket_tc15(mock_service):
    # TC15
    with pytest.raises(TypeError):
        update_ticket(1, [], service=mock_service)

# TC16: service.update_ticket()で業務例外発生（権限エラー等）
def test_update_ticket_tc16(mock_service_deskerror):
    # TC16
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(1, payload, service=mock_service_deskerror)

# TC17: 非常に大きいチケットIDかつtitle/descriptionが空文字
def test_update_ticket_tc17(mock_service_deskerror):
    # TC17
    payload = TicketUpdate("", "", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(999999, payload, service=mock_service_deskerror)

# TC18: 存在しないチケットIDかつpayload全項目がNone
def test_update_ticket_tc18(mock_service_valueerror):
    # TC18
    payload = TicketUpdate(None, None, None, None)
    with pytest.raises(ValueError):
        update_ticket(0, payload, service=mock_service_valueerror)

# TC19: 負のチケットIDかつpriorityが負の値
def test_update_ticket_tc19(mock_service_valueerror):
    # TC19
    payload = TicketUpdate("新しいタイトル", "新しい説明", -1, "user1")
    with pytest.raises(ValueError):
        update_ticket(-1, payload, service=mock_service_valueerror)

# TC20: ticket_idとpayloadが両方None
def test_update_ticket_tc20(mock_service):
    # TC20
    with pytest.raises(TypeError):
        update_ticket(None, None, service=mock_service)

# TC21: ticket_idとpayloadが両方型不一致
def test_update_ticket_tc21(mock_service):
    # TC21
    with pytest.raises(TypeError):
        update_ticket("abc", [], service=mock_service)

# TC22: service.update_ticket()でチケット不存在例外
def test_update_ticket_tc22(mock_service_deskerror_notfound):
    # TC22
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(1, payload, service=mock_service_deskerror_notfound)

# TC23: service.update_ticket()で権限エラー
def test_update_ticket_tc23(mock_service_deskerror_permission):
    # TC23
    payload = TicketUpdate("新しいタイトル", "新しい説明", 1, "user1")
    with pytest.raises(HTTPException):
        update_ticket(1, payload, service=mock_service_deskerror_permission)