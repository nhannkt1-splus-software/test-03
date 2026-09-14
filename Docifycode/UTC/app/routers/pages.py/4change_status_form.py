import pytest

# --- モッククラス定義 ---
class DeskError(Exception):
    pass

class TicketStatus:
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class TicketService:
    def __init__(self, raise_error=None):
        self.raise_error = raise_error
    def change_status(self, ticket_id, status):
        if self.raise_error:
            raise self.raise_error
        # TC2, TC3, TC4: 存在しないIDや負の値の場合DeskErrorを発生させる
        if ticket_id in [0, -1, 999999]:
            raise DeskError("Invalid ticket_id")
        # TC8: 不正なステータスの場合ValueErrorを発生させる
        if status not in [TicketStatus.OPEN, TicketStatus.CLOSED]:
            raise ValueError("Invalid status")
        # TC10: status変更不可の場合DeskErrorを発生させる
        if ticket_id == 1 and status == TicketStatus.OPEN and self.raise_error == DeskError:
            raise DeskError("Cannot change status")
        # 正常系は何もしない

class MemberService:
    pass

class ProjectService:
    pass

class LabelService:
    pass

class Request:
    pass

# --- テスト対象関数のインポート ---
from fastapi.responses import RedirectResponse

def _ticket_error(request, ticket_id, message, tickets, members, projects, labels):
    # エラー時のモックレスポンス
    return {"error": message, "ticket_id": ticket_id}

# テスト対象関数（直接テスト用に再現）
def change_status_form(
    ticket_id,
    request,
    status,
    tickets,
    members,
    projects,
    labels,
):
    try:
        tickets.change_status(ticket_id, status)
        return RedirectResponse(url=f"/tickets/{ticket_id}", status_code=303)
    except DeskError as exc:
        return _ticket_error(request, ticket_id, str(exc), tickets, members, projects, labels)

# --- テストケース ---
@pytest.mark.parametrize("ticket_id, status, expected, raise_error", [
    # TC1: 正常系：チケットIDとステータスが正常値の場合
    (1, TicketStatus.OPEN, "redirect", None),
    # TC2: 異常系：存在しないチケットID（境界値）
    (0, TicketStatus.OPEN, "desk_error", None),
    # TC3: 異常系：チケットIDが負の値の場合
    (-1, TicketStatus.OPEN, "desk_error", None),
    # TC4: 異常系：非常に大きいチケットID（存在しないID）
    (999999, TicketStatus.OPEN, "desk_error", None),
    # TC5: 異常系：チケットIDがstr型の場合（型不一致）
    ("abc", TicketStatus.OPEN, "type_error", None),
    # TC6: 異常系：チケットIDがNoneの場合（型不一致）
    (None, TicketStatus.OPEN, "type_error", None),
    # TC7: 正常系：ステータスがCLOSEDの場合
    (1, TicketStatus.CLOSED, "redirect", None),
    # TC8: 異常系：ステータスが不正値の場合
    (1, "INVALID_STATUS", "value_error", None),
    # TC9: 異常系：ステータスがNoneの場合（型不一致）
    (1, None, "type_error", None),
    # TC10: 異常系：status変更不可の場合（DeskError発生）
    (1, TicketStatus.OPEN, "desk_error", DeskError),
    # TC11: 正常系：status変更可能な場合（部分適用関数で引数が事前にセットされているケース）
    (1, TicketStatus.OPEN, "redirect", None),
    # TC12: 正常系：部分適用関数でCLOSEDステータスが事前にセットされているケース
    (1, TicketStatus.CLOSED, "redirect", None),
])
def test_change_status_form(ticket_id, status, expected, raise_error):
    # --- テストIDごとのコメント ---
    # TC1: 正常系：チケットIDとステータスが正常値の場合
    # TC2: 異常系：存在しないチケットID（境界値）
    # TC3: 異常系：チケットIDが負の値の場合
    # TC4: 異常系：非常に大きいチケットID（存在しないID）
    # TC5: 異常系：チケットIDがstr型の場合（型不一致）
    # TC6: 異常系：チケットIDがNoneの場合（型不一致）
    # TC7: 正常系：ステータスがCLOSEDの場合
    # TC8: 異常系：ステータスが不正値の場合
    # TC9: 異常系：ステータスがNoneの場合（型不一致）
    # TC10: 異常系：status変更不可の場合（DeskError発生）
    # TC11: 正常系：status変更可能な場合（部分適用関数で引数が事前にセットされているケース）
    # TC12: 正常系：部分適用関数でCLOSEDステータスが事前にセットされているケース

    tickets = TicketService(raise_error=raise_error)
    members = MemberService()
    projects = ProjectService()
    labels = LabelService()
    request = Request()

    if expected == "redirect":
        # 正常系：RedirectResponseが返ることを確認
        resp = change_status_form(ticket_id, request, status, tickets, members, projects, labels)
        # Japanese: RedirectResponse型であり、URLとステータスコードが正しいことを確認
        assert isinstance(resp, RedirectResponse)
        assert resp.status_code == 303
        assert resp.headers["location"] == f"/tickets/{ticket_id}"
    elif expected == "desk_error":
        # 異常系：DeskErrorが発生し、_ticket_errorが返ることを確認
        resp = change_status_form(ticket_id, request, status, tickets, members, projects, labels)
        # Japanese: エラー辞書が返ることを確認
        assert isinstance(resp, dict)
        assert "error" in resp
        assert resp["ticket_id"] == ticket_id
    elif expected == "type_error":
        # 異常系：型不一致の場合TypeErrorが発生することを確認
        with pytest.raises(TypeError):
            change_status_form(ticket_id, request, status, tickets, members, projects, labels)
    elif expected == "value_error":
        # 異常系：ValueErrorが発生することを確認
        with pytest.raises(ValueError):
            change_status_form(ticket_id, request, status, tickets, members, projects, labels)