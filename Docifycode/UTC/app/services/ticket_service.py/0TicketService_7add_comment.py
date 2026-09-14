import pytest

# --- テスト用ダミークラス・例外定義 ---

class NotFoundError(Exception):
    pass

class TicketClosedError(Exception):
    pass

class Comment:
    def __init__(self, body, author):
        self.body = body
        self.author = author

class DummyTicket:
    def __init__(self, ticket_id, closed=False):
        self.ticket_id = ticket_id
        self.closed = closed
        self.comments = []

    def add_comment(self, body, author):
        # body, authorはadd_comment前にstripされている前提
        if not body:
            raise ValueError("body must not be empty")
        if not author:
            raise ValueError("author must not be empty")
        comment = Comment(body, author)
        self.comments.append(comment)
        return comment

# --- TicketServiceのテスト用サブクラス ---

from types import MethodType

class TestableTicketService:
    """
    TicketServiceのテスト用サブクラス
    get_ticket, _ensure_not_closedをテスト用に差し替え
    """
    def __init__(self):
        # チケットID: DummyTicket
        self.tickets = {
            1: DummyTicket(1, closed=False),
            100: DummyTicket(100, closed=True),
        }

    def get_ticket(self, ticket_id):
        # 型チェック
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        if ticket_id <= 0:
            raise NotFoundError("ticket not found")
        if ticket_id not in self.tickets:
            raise NotFoundError("ticket not found")
        return self.tickets[ticket_id]

    def _ensure_not_closed(self, ticket, action):
        if getattr(ticket, "closed", False):
            raise TicketClosedError("ticket is closed")

    # 本物のadd_commentをそのまま使う
    from types import MethodType
    # 本物のTicketService.add_commentをバインド
    # テストクラスのインスタンスにバインドする
    # テストクラスのインスタンスで呼び出せるようにする
    # テストクラスのインスタンスのselfを渡す
    # テストクラスのインスタンスのselfを渡す
    # テストクラスのインスタンスのselfを渡す
    # テストクラスのインスタンスのselfを渡す

import sys
import types

from inspect import isfunction

# TicketServiceクラスをimport
from types import SimpleNamespace

# 本物のTicketService.add_commentをTestableTicketServiceにバインド
import builtins

# --- 本物のTicketService.add_commentをTestableTicketServiceにバインド ---
import sys

# TicketServiceクラスをグローバル名前空間から取得
TicketService = None
for obj in list(globals().values()):
    if isinstance(obj, type) and obj.__name__ == "TicketService":
        TicketService = obj
        break
if TicketService is None:
    # pytestでimportされる場合
    import __main__
    for obj in list(vars(__main__).values()):
        if isinstance(obj, type) and obj.__name__ == "TicketService":
            TicketService = obj
            break

TestableTicketService.add_comment = TicketService.add_comment

# --- pytest用テスト関数 ---

# --- 正常系 ---

# TC1: 正常系：全ての入力が正しい場合
def test_add_comment_TC1():
    # テストID: TC1
    service = TestableTicketService()
    result = service.add_comment(1, "コメント本文", "author_name")
    # コメントが追加されていること
    assert isinstance(result, Comment)
    assert result.body == "コメント本文"
    assert result.author == "author_name"

# TC2: 正常系：body, authorの前後に空白がある場合
def test_add_comment_TC2():
    # テストID: TC2
    service = TestableTicketService()
    result = service.add_comment(1, "   コメント本文   ", "   author_name   ")
    assert isinstance(result, Comment)
    assert result.body == "コメント本文"
    assert result.author == "author_name"

# --- 異常系 ---

# TC3: bodyが空文字列の場合
def test_add_comment_TC3():
    # テストID: TC3
    service = TestableTicketService()
    with pytest.raises(ValueError):
        service.add_comment(1, "", "author_name")

# TC4: authorが空文字列の場合
def test_add_comment_TC4():
    # テストID: TC4
    service = TestableTicketService()
    with pytest.raises(ValueError):
        service.add_comment(1, "コメント本文", "")

# TC5: bodyが空白・改行・タブのみの場合
def test_add_comment_TC5():
    # テストID: TC5
    service = TestableTicketService()
    with pytest.raises(ValueError):
        service.add_comment(1, "\n\t ", "author_name")

# TC6: bodyがNoneの場合
def test_add_comment_TC6():
    # テストID: TC6
    service = TestableTicketService()
    with pytest.raises(AttributeError):
        service.add_comment(1, None, "author_name")

# TC7: bodyがint型の場合
def test_add_comment_TC7():
    # テストID: TC7
    service = TestableTicketService()
    with pytest.raises(AttributeError):
        service.add_comment(1, 123, "author_name")

# TC8: authorがNoneの場合
def test_add_comment_TC8():
    # テストID: TC8
    service = TestableTicketService()
    with pytest.raises(AttributeError):
        service.add_comment(1, "コメント本文", None)

# TC9: authorがint型の場合
def test_add_comment_TC9():
    # テストID: TC9
    service = TestableTicketService()
    with pytest.raises(AttributeError):
        service.add_comment(1, "コメント本文", 456)

# TC10: 存在しないチケットID
def test_add_comment_TC10():
    # テストID: TC10
    service = TestableTicketService()
    with pytest.raises(NotFoundError):
        service.add_comment(9999, "コメント本文", "author_name")

# TC11: 負のチケットID
def test_add_comment_TC11():
    # テストID: TC11
    service = TestableTicketService()
    with pytest.raises(NotFoundError):
        service.add_comment(-1, "コメント本文", "author_name")

# TC12: 0のチケットID
def test_add_comment_TC12():
    # テストID: TC12
    service = TestableTicketService()
    with pytest.raises(NotFoundError):
        service.add_comment(0, "コメント本文", "author_name")

# TC13: ticket_idがstr型の場合
def test_add_comment_TC13():
    # テストID: TC13
    service = TestableTicketService()
    with pytest.raises(TypeError):
        service.add_comment("1", "コメント本文", "author_name")

# TC14: ticket_idがNone型の場合
def test_add_comment_TC14():
    # テストID: TC14
    service = TestableTicketService()
    with pytest.raises(TypeError):
        service.add_comment(None, "コメント本文", "author_name")

# TC15: ticket_idがfloat型の場合
def test_add_comment_TC15():
    # テストID: TC15
    service = TestableTicketService()
    with pytest.raises(TypeError):
        service.add_comment(2.5, "コメント本文", "author_name")

# TC16: チケットがclosedの場合
def test_add_comment_TC16():
    # テストID: TC16
    service = TestableTicketService()
    with pytest.raises(TicketClosedError):
        service.add_comment(100, "コメント本文", "author_name")

# --- 部分適用系 ---

# TC17: 部分適用：ticket_id, body, authorを固定してadd_commentを部分適用した場合の正常系
def test_add_comment_TC17():
    # テストID: TC17
    service = TestableTicketService()
    from functools import partial
    partial_add_comment = partial(service.add_comment, 1, "コメント本文", "author_name")
    result = partial_add_comment()
    assert isinstance(result, Comment)
    assert result.body == "コメント本文"
    assert result.author == "author_name"

# TC18: 部分適用：body, authorに前後空白がある場合の部分適用
def test_add_comment_TC18():
    # テストID: TC18
    service = TestableTicketService()
    from functools import partial
    partial_add_comment = partial(service.add_comment, 1, "   コメント本文   ", "   author_name   ")
    result = partial_add_comment()
    assert isinstance(result, Comment)
    assert result.body == "コメント本文"
    assert result.author == "author_name"

# TC19: 部分適用：bodyが空文字列の場合の部分適用
def test_add_comment_TC19():
    # テストID: TC19
    service = TestableTicketService()
    from functools import partial
    partial_add_comment = partial(service.add_comment, 1, "", "author_name")
    with pytest.raises(ValueError):
        partial_add_comment()

# TC20: 部分適用：authorが空文字列の場合の部分適用
def test_add_comment_TC20():
    # テストID: TC20
    service = TestableTicketService()
    from functools import partial
    partial_add_comment = partial(service.add_comment, 1, "コメント本文", "")
    with pytest.raises(ValueError):
        partial_add_comment()

# TC21: 部分適用：チケットがclosedの場合の部分適用
def test_add_comment_TC21():
    # テストID: TC21
    service = TestableTicketService()
    from functools import partial
    partial_add_comment = partial(service.add_comment, 100, "コメント本文", "author_name")
    with pytest.raises(TicketClosedError):
        partial_add_comment()
```
