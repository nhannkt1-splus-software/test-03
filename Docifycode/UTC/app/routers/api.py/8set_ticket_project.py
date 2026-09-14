import pytest
from unittest.mock import Mock, create_autospec

# --- テスト用のダミークラス・関数定義 ---
# 本来はimportするが、テストのためにダミーを定義
class DeskError(Exception):
    pass

def http_error(exc):
    # DeskErrorをHTTP例外に変換するダミー関数
    return Exception("HTTP Error: " + str(exc))

class TicketOut:
    # ダミーの戻り値用クラス
    def __init__(self, ticket_id, project_id):
        self.ticket_id = ticket_id
        self.project_id = project_id

    def __eq__(self, other):
        return (
            isinstance(other, TicketOut)
            and self.ticket_id == other.ticket_id
            and self.project_id == other.project_id
        )

class TicketProjectChange:
    # payload用のダミークラス
    def __init__(self, project_id):
        self.project_id = project_id

class TicketService:
    # service用のダミークラス
    def set_project(self, ticket_id, project_id):
        # 実際の挙動はテストごとにMockで差し替える
        pass

def to_ticket_out(ticket):
    # service.set_projectの戻り値をTicketOutに変換するダミー関数
    return ticket

# --- テスト対象関数のimport ---
# 本来は from ... import set_ticket_project だが、ここでは直接定義
def set_ticket_project(
    ticket_id,
    payload,
    service,
):
    try:
        return to_ticket_out(service.set_project(ticket_id, payload.project_id))
    except DeskError as exc:
        raise http_error(exc) from exc

# --- 各テストケース ---

# TC1: 正常系: チケットID・プロジェクトIDともに正常値
def test_set_ticket_project_TC1():
    # TC1
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = 1
    expected_ticket = TicketOut(ticket_id, 10)
    service.set_project.return_value = expected_ticket

    # 実行
    result = set_ticket_project(ticket_id, payload, service)

    # 検証
    assert result == expected_ticket

# TC2: 異常系: 存在しないチケットID（境界値）
def test_set_ticket_project_TC2():
    # TC2
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = 0
    service.set_project.side_effect = DeskError("not found")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    # DeskErrorはhttp_errorでExceptionに変換される
    assert "HTTP Error" in str(excinfo.value)

# TC3: 異常系: チケットIDが負の整数
def test_set_ticket_project_TC3():
    # TC3
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = -1
    service.set_project.side_effect = DeskError("negative id")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC4: 異常系: チケットIDが非常に大きい整数値
def test_set_ticket_project_TC4():
    # TC4
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = 999999
    service.set_project.side_effect = DeskError("not found")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC5: 異常系: チケットIDが型不一致（str）
def test_set_ticket_project_TC5():
    # TC5
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = "abc"
    # set_project呼び出し時にTypeErrorが発生する想定
    service.set_project.side_effect = TypeError("ticket_id must be int")

    with pytest.raises(TypeError):
        set_ticket_project(ticket_id, payload, service)

# TC6: 異常系: チケットIDがNone
def test_set_ticket_project_TC6():
    # TC6
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = None
    service.set_project.side_effect = TypeError("ticket_id must be int")

    with pytest.raises(TypeError):
        set_ticket_project(ticket_id, payload, service)

# TC7: 異常系: project_idが存在しないプロジェクトID（境界値）
def test_set_ticket_project_TC7():
    # TC7
    service = create_autospec(TicketService)
    payload = TicketProjectChange(0)
    ticket_id = 1
    service.set_project.side_effect = DeskError("project not found")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC8: 異常系: project_idが負の整数
def test_set_ticket_project_TC8():
    # TC8
    service = create_autospec(TicketService)
    payload = TicketProjectChange(-5)
    ticket_id = 1
    service.set_project.side_effect = DeskError("invalid project id")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC9: 異常系: project_idが非常に大きい整数値
def test_set_ticket_project_TC9():
    # TC9
    service = create_autospec(TicketService)
    payload = TicketProjectChange(999999)
    ticket_id = 1
    service.set_project.side_effect = DeskError("project not found")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC10: 異常系: project_idが型不一致（str）
def test_set_ticket_project_TC10():
    # TC10
    service = create_autospec(TicketService)
    payload = TicketProjectChange("xyz")
    ticket_id = 1
    service.set_project.side_effect = TypeError("project_id must be int")

    with pytest.raises(TypeError):
        set_ticket_project(ticket_id, payload, service)

# TC11: 異常系: payloadがNone
def test_set_ticket_project_TC11():
    # TC11
    service = create_autospec(TicketService)
    payload = None
    ticket_id = 1

    with pytest.raises(TypeError):
        set_ticket_project(ticket_id, payload, service)

# TC12: 異常系: serviceが異常なインスタンス（set_projectが例外を投げる）
def test_set_ticket_project_TC12():
    # TC12
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = 1
    service.set_project.side_effect = DeskError("service error")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC13: 異常系: チケットIDとproject_idが両方とも境界値（存在しないID）
def test_set_ticket_project_TC13():
    # TC13
    service = create_autospec(TicketService)
    payload = TicketProjectChange(0)
    ticket_id = 0
    service.set_project.side_effect = DeskError("not found")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC14: 異常系: チケットIDとproject_idが両方とも負の整数
def test_set_ticket_project_TC14():
    # TC14
    service = create_autospec(TicketService)
    payload = TicketProjectChange(-5)
    ticket_id = -1
    service.set_project.side_effect = DeskError("invalid id")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC15: 異常系: チケットIDとproject_idが両方とも非常に大きい整数値
def test_set_ticket_project_TC15():
    # TC15
    service = create_autospec(TicketService)
    payload = TicketProjectChange(999999)
    ticket_id = 999999
    service.set_project.side_effect = DeskError("not found")

    with pytest.raises(Exception) as excinfo:
        set_ticket_project(ticket_id, payload, service)
    assert "HTTP Error" in str(excinfo.value)

# TC16: 異常系: ticket_idとproject_idが両方とも型不一致（str）
def test_set_ticket_project_TC16():
    # TC16
    service = create_autospec(TicketService)
    payload = TicketProjectChange("xyz")
    ticket_id = "abc"
    service.set_project.side_effect = TypeError("ticket_id and project_id must be int")

    with pytest.raises(TypeError):
        set_ticket_project(ticket_id, payload, service)

# TC17: 異常系: ticket_idとpayloadが両方ともNone
def test_set_ticket_project_TC17():
    # TC17
    service = create_autospec(TicketService)
    payload = None
    ticket_id = None

    with pytest.raises(TypeError):
        set_ticket_project(ticket_id, payload, service)

# TC18: 異常系: service.set_projectがDeskError以外の例外を投げるケース
def test_set_ticket_project_TC18():
    # TC18
    service = create_autospec(TicketService)
    payload = TicketProjectChange(10)
    ticket_id = 1
    service.set_project.side_effect = ValueError("unexpected error")

    with pytest.raises(ValueError):
        set_ticket_project(ticket_id, payload, service)
```
