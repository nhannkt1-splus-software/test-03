import pytest
from unittest.mock import patch, MagicMock

# テスト用のダミーTicketクラスを定義
class Ticket:
    def __init__(self, ticket_id, status="open", assignee=None, updated_at=None):
        self.id = ticket_id
        self.status = status
        self.assignee = assignee
        self.updated_at = updated_at

# テスト対象クラスのimport
from target_module import TicketService  # 実際のモジュール名に合わせて修正してください

# --- 正常系 ---

# TC1: チケットがオープンで、usernameが正常な場合
def test_assign_TC1():
    # チケットインスタンスを作成
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket) as mock_get_ticket, \
         patch.object(service, '_ensure_not_closed', return_value=None) as mock_ensure, \
         patch.object(service, '_resolve_assignee', return_value="user1") as mock_resolve, \
         patch('target_module.utc_now', return_value="2024-06-01T12:00:00Z") as mock_utc_now:
        # 実行
        result = service.assign(1, "user1")
        # 検証
        assert result is ticket
        assert ticket.assignee == "user1"
        assert ticket.updated_at == "2024-06-01T12:00:00Z"
        mock_get_ticket.assert_called_once_with(1)
        mock_ensure.assert_called_once_with(ticket, "assign")
        mock_resolve.assert_called_once_with("user1")
        mock_utc_now.assert_called_once()

# TC2: usernameが空文字の場合
def test_assign_TC2():
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None), \
         patch.object(service, '_resolve_assignee', return_value=""), \
         patch('target_module.utc_now', return_value="2024-06-01T12:00:00Z"):
        result = service.assign(1, "")
        assert result is ticket
        assert ticket.assignee == ""
        assert ticket.updated_at == "2024-06-01T12:00:00Z"

# TC3: usernameがNoneの場合
def test_assign_TC3():
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None), \
         patch.object(service, '_resolve_assignee', return_value=None), \
         patch('target_module.utc_now', return_value="2024-06-01T12:00:00Z"):
        result = service.assign(1, None)
        assert result is ticket
        assert ticket.assignee is None
        assert ticket.updated_at == "2024-06-01T12:00:00Z"

# TC14: updated_atが正しく更新されることを確認
def test_assign_TC14():
    ticket = Ticket(1, status="open", assignee=None, updated_at="old_time")
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None), \
         patch.object(service, '_resolve_assignee', return_value="user1"), \
         patch('target_module.utc_now', return_value="2024-06-01T12:00:00Z"):
        result = service.assign(1, "user1")
        assert ticket.updated_at == "2024-06-01T12:00:00Z"

# TC15: assigneeが既に設定されているチケットに再度assignするケース
def test_assign_TC15():
    ticket = Ticket(1, status="open", assignee="old_user")
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None), \
         patch.object(service, '_resolve_assignee', return_value="user1"), \
         patch('target_module.utc_now', return_value="2024-06-01T12:00:00Z"):
        result = service.assign(1, "user1")
        assert ticket.assignee == "user1"
        assert ticket.updated_at == "2024-06-01T12:00:00Z"

# TC16: assigneeがNoneのチケットにassignするケース
def test_assign_TC16():
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None), \
         patch.object(service, '_resolve_assignee', return_value="user1"), \
         patch('target_module.utc_now', return_value="2024-06-01T12:00:00Z"):
        result = service.assign(1, "user1")
        assert ticket.assignee == "user1"
        assert ticket.updated_at == "2024-06-01T12:00:00Z"

# --- 異常系 ---

# TC4: チケットがクローズ状態の場合
def test_assign_TC4():
    ticket = Ticket(1, status="closed", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', side_effect=Exception("Ticket is closed")):
        with pytest.raises(Exception) as excinfo:
            service.assign(1, "user1")
        assert str(excinfo.value) == "Ticket is closed"

# TC5: チケットが存在しない場合
def test_assign_TC5():
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=None):
        with pytest.raises(Exception) as excinfo:
            service.assign(0, "user1")
        assert str(excinfo.value) == "Ticket not found"

# TC6: usernameが不正な場合
def test_assign_TC6():
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None), \
         patch.object(service, '_resolve_assignee', side_effect=Exception("Invalid username")):
        with pytest.raises(Exception) as excinfo:
            service.assign(1, "invalid_user")
        assert str(excinfo.value) == "Invalid username"

# TC7: ticket_idが負の整数値で存在しない場合
def test_assign_TC7():
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=None):
        with pytest.raises(Exception) as excinfo:
            service.assign(-1, "user1")
        assert str(excinfo.value) == "Ticket not found"

# TC8: ticket_idが非常に大きい整数値で存在しない場合
def test_assign_TC8():
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=None):
        with pytest.raises(Exception) as excinfo:
            service.assign(999999, "user1")
        assert str(excinfo.value) == "Ticket not found"

# TC9: ticket_idが文字列型（型不一致）の場合
def test_assign_TC9():
    service = TicketService()
    with pytest.raises(TypeError):
        service.assign("abc", "user1")

# TC10: ticket_idがNoneの場合
def test_assign_TC10():
    service = TicketService()
    with pytest.raises(TypeError):
        service.assign(None, "user1")

# TC11: ticket_idが浮動小数点数の場合
def test_assign_TC11():
    service = TicketService()
    with pytest.raises(TypeError):
        service.assign(2.5, "user1")

# TC12: usernameが整数型の場合
def test_assign_TC12():
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None):
        with pytest.raises(TypeError):
            service.assign(1, 123)

# TC13: usernameがリスト型の場合
def test_assign_TC13():
    ticket = Ticket(1, status="open", assignee=None)
    service = TicketService()
    with patch.object(service, 'get_ticket', return_value=ticket), \
         patch.object(service, '_ensure_not_closed', return_value=None):
        with pytest.raises(TypeError):
            service.assign(1, [])