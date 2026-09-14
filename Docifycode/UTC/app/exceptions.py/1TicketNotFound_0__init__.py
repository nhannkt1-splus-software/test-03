import pytest

# DeskErrorが未定義の場合、テスト用にダミー定義
class DeskError(Exception):
    pass

# TicketNotFoundクラスのテスト対象
from types import SimpleNamespace

# TicketNotFoundクラスがスコープ外の場合、リフレクション等でアクセスする必要があるが、
# ここでは直接定義されている前提でテストを記述

class TicketNotFound(DeskError):
    def __init__(self, ticket_id: int) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Ticket {ticket_id} was not found")

# 正常系：int型のticket_idを指定した場合
@pytest.mark.parametrize(
    "ticket_id, expected_message, test_id",
    [
        # TC1: 正のint型チケットID
        (1, "Ticket 1 was not found", "TC1"),
        # TC2: int型の境界値（0）
        (0, "Ticket 0 was not found", "TC2"),
        # TC3: int型の負のチケットID
        (-1, "Ticket -1 was not found", "TC3"),
        # TC4: 非常に大きいint型チケットID
        (999999999, "Ticket 999999999 was not found", "TC4"),
        # TC10: 部分適用：正のint型
        (1, "Ticket 1 was not found", "TC10"),
        # TC11: 部分適用：境界値0
        (0, "Ticket 0 was not found", "TC11"),
        # TC12: 部分適用：負のint型
        (-1, "Ticket -1 was not found", "TC12"),
        # TC13: 部分適用：非常に大きいint型
        (999999999, "Ticket 999999999 was not found", "TC13"),
    ]
)
def test_ticket_not_found_int_ticket_id(ticket_id, expected_message, test_id):
    # --- {test_id} ---
    # ticket_idがint型の場合、例外は発生せず、messageが正しく生成されることを確認
    tnf = TicketNotFound(ticket_id)
    assert tnf.ticket_id == ticket_id  # ticket_id属性が正しくセットされていること
    assert str(tnf) == expected_message  # 例外メッセージが正しいこと

# 異常系：ticket_idがint型以外の場合
@pytest.mark.parametrize(
    "ticket_id, test_id",
    [
        # TC5: None型（型不一致）
        (None, "TC5"),
        # TC6: str型（型不一致）
        ("abc", "TC6"),
        # TC7: float型（型不一致）
        (3.14, "TC7"),
        # TC8: list型（型不一致）
        ([], "TC8"),
        # TC9: dict型（型不一致）
        ({}, "TC9"),
        # TC14: 部分適用：None型（型不一致）
        (None, "TC14"),
        # TC15: 部分適用：str型（型不一致）
        ("abc", "TC15"),
        # TC16: 部分適用：float型（型不一致）
        (3.14, "TC16"),
        # TC17: 部分適用：list型（型不一致）
        ([], "TC17"),
        # TC18: 部分適用：dict型（型不一致）
        ({}, "TC18"),
    ]
)
def test_ticket_not_found_invalid_ticket_id(ticket_id, test_id):
    # --- {test_id} ---
    # ticket_idがint型以外の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        TicketNotFound(ticket_id)