import pytest
from unittest.mock import patch, MagicMock

# --- テスト用ダミークラス定義 ---

# Ticketクラスのダミー
class Ticket:
    def __init__(self, ticket_id, project_id, status, updated_at=None):
        self.ticket_id = ticket_id
        self.project_id = project_id
        self.status = status
        self.updated_at = updated_at

# utc_nowのダミー
def dummy_utc_now():
    return "2024-01-01T00:00:00Z"

# --- TicketServiceのテスト ---

from types import SimpleNamespace

@pytest.fixture
def ticket_service():
    # TicketServiceのインスタンスを返す
    from target import TicketService  # テスト対象のTicketServiceをimport
    return TicketService()

# get_ticketのモックを作成
def make_get_ticket_mock(tickets):
    """
    tickets: dict[ticket_id, Ticket or None]
    """
    def _get_ticket(ticket_id):
        # 型チェック
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        if ticket_id not in tickets or tickets[ticket_id] is None:
            raise ValueError("Ticket not found")
        return tickets[ticket_id]
    return _get_ticket

# _ensure_not_closedのモック
def make_ensure_not_closed_mock():
    def _ensure_not_closed(ticket, action):
        if ticket.status == "closed":
            raise ValueError("Ticket is closed")
    return _ensure_not_closed

# _resolve_project_idのモック
def make_resolve_project_id_mock(raise_exc=None):
    def _resolve_project_id(project_id):
        if raise_exc:
            raise raise_exc
        # 型チェック
        if project_id is not None and not isinstance(project_id, int):
            raise TypeError("project_id must be int or None")
        return project_id
    return _resolve_project_id

# --- 各テストケース ---

# TC1: 正常系: チケットID・プロジェクトIDともに正常な値、チケットがオープン状態
def test_set_project_TC1(ticket_service):
    # チケット準備
    ticket = Ticket(ticket_id=1, project_id=10, status="open")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()), \
         patch('target.utc_now', dummy_utc_now):
        # 実行
        result = ticket_service.set_project(1, 2)
        # 検証
        assert result is ticket
        assert result.project_id == 2
        assert result.updated_at == "2024-01-01T00:00:00Z"

# TC2: 正常系: project_idがNoneの場合
def test_set_project_TC2(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="open")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()), \
         patch('target.utc_now', dummy_utc_now):
        result = ticket_service.set_project(1, None)
        assert result is ticket
        assert result.project_id is None
        assert result.updated_at == "2024-01-01T00:00:00Z"

# TC3: 正常系: project_idが負の値（許容される場合）
def test_set_project_TC3(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="open")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()), \
         patch('target.utc_now', dummy_utc_now):
        result = ticket_service.set_project(1, -1)
        assert result is ticket
        assert result.project_id == -1
        assert result.updated_at == "2024-01-01T00:00:00Z"

# TC4: 正常系: project_idが非常に大きい値（許容される場合）
def test_set_project_TC4(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="open")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()), \
         patch('target.utc_now', dummy_utc_now):
        result = ticket_service.set_project(1, 999999)
        assert result is ticket
        assert result.project_id == 999999
        assert result.updated_at == "2024-01-01T00:00:00Z"

# TC5: 異常系: チケットがクローズ状態
def test_set_project_TC5(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="closed")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(1, 2)

# TC6: 異常系: 存在しないチケットID
def test_set_project_TC6(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(0, 2)

# TC7: 異常系: ticket_idが負の値で存在しない場合
def test_set_project_TC7(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(-1, 2)

# TC8: 異常系: ticket_idが非常に大きい値で存在しない場合
def test_set_project_TC8(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(999999, 2)

# TC9: 異常系: ticket_idが文字列型（型不一致）
def test_set_project_TC9(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project("abc", 2)

# TC10: 異常系: ticket_idがNoneの場合
def test_set_project_TC10(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project(None, 2)

# TC11: 異常系: project_idが文字列型（型不一致）
def test_set_project_TC11(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="open")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project(1, "xyz")

# TC12: 異常系: project_idが不正な場合（_resolve_project_idで例外）
def test_set_project_TC12(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="open")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock(raise_exc=ValueError("invalid project_id"))):
        with pytest.raises(ValueError):
            ticket_service.set_project(1, 2)

# TC13: 異常系: チケットがクローズ状態かつproject_idがNoneの場合
def test_set_project_TC13(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="closed")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(1, None)

# TC14: 異常系: チケットがクローズ状態かつproject_idが負の値の場合
def test_set_project_TC14(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="closed")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(1, -1)

# TC15: 異常系: チケットがクローズ状態かつproject_idが非常に大きい値の場合
def test_set_project_TC15(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="closed")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(1, 999999)

# TC16: 異常系: 存在しないチケットIDかつproject_idがNoneの場合
def test_set_project_TC16(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(0, None)

# TC17: 異常系: ticket_idが負の値かつproject_idがNoneの場合
def test_set_project_TC17(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(-1, None)

# TC18: 異常系: ticket_idが非常に大きい値かつproject_idがNoneの場合
def test_set_project_TC18(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(999999, None)

# TC19: 異常系: 存在しないチケットIDかつproject_idが負の値の場合
def test_set_project_TC19(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(0, -1)

# TC20: 異常系: ticket_idが負の値かつproject_idが負の値の場合
def test_set_project_TC20(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(-1, -1)

# TC21: 異常系: ticket_idが非常に大きい値かつproject_idが負の値の場合
def test_set_project_TC21(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(999999, -1)

# TC22: 異常系: 存在しないチケットIDかつproject_idが非常に大きい値の場合
def test_set_project_TC22(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(0, 999999)

# TC23: 異常系: ticket_idが負の値かつproject_idが非常に大きい値の場合
def test_set_project_TC23(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(-1, 999999)

# TC24: 異常系: ticket_idが非常に大きい値かつproject_idが非常に大きい値の場合
def test_set_project_TC24(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(ValueError):
            ticket_service.set_project(999999, 999999)

# TC25: 異常系: ticket_idが文字列型かつproject_idがNoneの場合
def test_set_project_TC25(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project("abc", None)

# TC26: 異常系: ticket_idがNoneかつproject_idがNoneの場合
def test_set_project_TC26(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project(None, None)

# TC27: 異常系: ticket_idが文字列型かつproject_idが負の値の場合
def test_set_project_TC27(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project("abc", -1)

# TC28: 異常系: ticket_idがNoneかつproject_idが負の値の場合
def test_set_project_TC28(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project(None, -1)

# TC29: 異常系: ticket_idが文字列型かつproject_idが非常に大きい値の場合
def test_set_project_TC29(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project("abc", 999999)

# TC30: 異常系: ticket_idがNoneかつproject_idが非常に大きい値の場合
def test_set_project_TC30(ticket_service):
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        with pytest.raises(TypeError):
            ticket_service.set_project(None, 999999)

# TC31: 異常系: チケットがクローズ状態かつproject_idが文字列型（型不一致）
def test_set_project_TC31(ticket_service):
    ticket = Ticket(ticket_id=1, project_id=10, status="closed")
    with patch.object(ticket_service, 'get_ticket', make_get_ticket_mock({1: ticket})), \
         patch.object(ticket_service, '_ensure_not_closed', make_ensure_not_closed_mock()), \
         patch.object(ticket_service, '_resolve_project_id', make_resolve_project_id_mock()):
        # _ensure_not_closedが先にValueErrorをraiseする
        with pytest.raises(ValueError):
            ticket_service.set_project(1, "xyz")