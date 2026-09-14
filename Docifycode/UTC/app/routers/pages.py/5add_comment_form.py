import pytest

# --- モッククラス定義 ---
class DeskError(Exception):
    pass

class TicketService:
    def __init__(self, valid_ticket_ids=None):
        self.valid_ticket_ids = valid_ticket_ids or {1}
        self.comments = {}

    def add_comment(self, ticket_id, body, author):
        # チケットID存在チェック
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        if ticket_id not in self.valid_ticket_ids or ticket_id <= 0:
            raise DeskError("Ticket not found")
        # body/authorチェック
        if body is None:
            raise TypeError("body must not be None")
        if author is None:
            raise TypeError("author must not be None")
        if isinstance(body, str) and body.strip() == "":
            raise DeskError("body must not be empty or whitespace")
        if isinstance(author, str) and author.strip() == "":
            raise DeskError("author must not be empty or whitespace")
        # body/author型チェック
        if not isinstance(body, str):
            raise TypeError("body must be str")
        if not isinstance(author, str):
            raise TypeError("author must be str")
        # コメント追加
        self.comments.setdefault(ticket_id, []).append((body, author))

class MemberService:
    pass

class ProjectService:
    pass

class LabelService:
    pass

class Request:
    pass

# --- テスト対象関数 ---
from fastapi.responses import RedirectResponse

def _ticket_error(request, ticket_id, error_message, tickets, members, projects, labels):
    # エラー時のダミー戻り値
    return {"error": error_message, "ticket_id": ticket_id}

def add_comment_form(
    ticket_id,
    request,
    body,
    author,
    tickets,
    members,
    projects,
    labels,
):
    try:
        tickets.add_comment(ticket_id, body, author)
        return RedirectResponse(url=f"/tickets/{ticket_id}", status_code=303)
    except DeskError as exc:
        return _ticket_error(request, ticket_id, str(exc), tickets, members, projects, labels)

# --- テストケース ---
@pytest.mark.parametrize("test_id, author, body, labels, members, projects, request, ticket_id, tickets, expected", [
    # TC1: 正常系
    ("TC1", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), None),
    # TC2: 存在しないチケットID
    ("TC2", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 9999, TicketService({1}), DeskError),
    # TC3: bodyが空文字
    ("TC3", "user1", "", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), DeskError),
    # TC4: authorが空文字
    ("TC4", "", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), DeskError),
    # TC5: ticket_idがstr型（型不正）
    ("TC5", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), "abc", TicketService({1}), TypeError),
    # TC6: bodyがNone
    ("TC6", "user1", None, LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), TypeError),
    # TC7: authorがNone
    ("TC7", None, "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), TypeError),
    # TC8: bodyが非常に長い場合
    ("TC8", "user1", "a" * 10000, LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), None),
    # TC9: requestがNone
    ("TC9", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), None, 1, TicketService({1}), TypeError),
    # TC10: ticketsがNone
    ("TC10", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 1, None, TypeError),
    # TC11: membersがNone
    ("TC11", "user1", "valid comment", LabelService(), None, ProjectService(), Request(), 1, TicketService({1}), TypeError),
    # TC12: projectsがNone
    ("TC12", "user1", "valid comment", LabelService(), MemberService(), None, Request(), 1, TicketService({1}), TypeError),
    # TC13: labelsがNone
    ("TC13", "user1", "valid comment", None, MemberService(), ProjectService(), Request(), 1, TicketService({1}), TypeError),
    # TC14: ticket_idが0（存在しないID）
    ("TC14", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 0, TicketService({1}), DeskError),
    # TC15: ticket_idが負の値
    ("TC15", "user1", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), -1, TicketService({1}), DeskError),
    # TC16: bodyが空白のみ
    ("TC16", "user1", "    ", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), DeskError),
    # TC17: authorが空白のみ
    ("TC17", "    ", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), DeskError),
    # TC18: authorに特殊文字（日本語や記号）
    ("TC18", "ユーザー#1!@#$", "valid comment", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), None),
    # TC19: bodyに特殊文字
    ("TC19", "user1", "!@#$%^&*()", LabelService(), MemberService(), ProjectService(), Request(), 1, TicketService({1}), None),
])
def test_add_comment_form(test_id, author, body, labels, members, projects, request, ticket_id, tickets, expected):
    # --- テストIDコメント ---
    # テストID: {test_id}
    # 入力値: author={author}, body={body}, labels={labels}, members={members}, projects={projects}, request={request}, ticket_id={ticket_id}, tickets={tickets}
    # 期待値: {expected}
    # --- テスト実施 ---
    # TypeError系
    if test_id in ["TC5", "TC6", "TC7", "TC9", "TC10", "TC11", "TC12", "TC13"]:
        with pytest.raises(TypeError):
            add_comment_form(ticket_id, request, body, author, tickets, members, projects, labels)
    # DeskError系
    elif test_id in ["TC2", "TC3", "TC4", "TC14", "TC15", "TC16", "TC17"]:
        result = add_comment_form(ticket_id, request, body, author, tickets, members, projects, labels)
        # エラー戻り値の検証
        assert isinstance(result, dict)
        assert "error" in result
        assert "ticket_id" in result
    # 正常系
    else:
        result = add_comment_form(ticket_id, request, body, author, tickets, members, projects, labels)
        # RedirectResponseの検証
        assert isinstance(result, RedirectResponse)
        assert result.status_code == 303
        assert result.headers["location"] == f"/tickets/{ticket_id}"