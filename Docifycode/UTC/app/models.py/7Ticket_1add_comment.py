import pytest
from datetime import datetime, timedelta, timezone

# --- 必要なクラス・関数のダミー定義（テスト対象のスコープ外でimportされている前提） ---
# 本来はテスト対象モジュールからimportする
from target_module import Ticket, Comment  # 例: テスト対象のモジュール名に合わせて修正

# utc_now() のダミー（本来はテスト対象からimport）
def utc_now():
    return datetime.now(timezone.utc)

# --- テストケース ---

# TC1: 正常系：本文と著者名が通常の文字列
def test_add_comment_normal_case():
    # TC1
    ticket = Ticket(id=1, title="t", description="d")
    author = "user1"
    body = "テストコメント"
    comment = ticket.add_comment(body=body, author=author)
    # コメント内容の検証
    assert comment.body == body  # 本文が一致
    assert comment.author == author  # 著者名が一致
    assert comment.id == 1  # 最初のコメントID
    assert ticket.comments[-1] == comment  # チケットに追加されている
    # updated_atが更新されていること
    assert abs((ticket.updated_at - utc_now()).total_seconds()) < 5  # 5秒以内

# TC2: 本文が空文字列
def test_add_comment_empty_body():
    # TC2
    ticket = Ticket(id=2, title="t", description="d")
    author = "user1"
    body = ""
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == ""
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC3: 著者名が空文字列
def test_add_comment_empty_author():
    # TC3
    ticket = Ticket(id=3, title="t", description="d")
    author = ""
    body = "テストコメント"
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == ""
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC4: 本文・著者名ともに空文字列
def test_add_comment_empty_body_and_author():
    # TC4
    ticket = Ticket(id=4, title="t", description="d")
    author = ""
    body = ""
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == ""
    assert comment.author == ""
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC5: 本文が非常に長い文字列
def test_add_comment_long_body():
    # TC5
    ticket = Ticket(id=5, title="t", description="d")
    author = "user1"
    body = "a" * 1000
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC6: 著者名が非常に長い文字列
def test_add_comment_long_author():
    # TC6
    ticket = Ticket(id=6, title="t", description="d")
    author = "a" * 100
    body = "テストコメント"
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC7: 本文が特殊文字を含む
def test_add_comment_special_char_body():
    # TC7
    ticket = Ticket(id=7, title="t", description="d")
    author = "user1"
    body = "!@#$%^&*()_+"
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC8: 著者名が特殊文字を含む
def test_add_comment_special_char_author():
    # TC8
    ticket = Ticket(id=8, title="t", description="d")
    author = "ユーザー#1!"
    body = "テストコメント"
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC9: 本文がNone型（型違いエラー）
def test_add_comment_body_none():
    # TC9
    ticket = Ticket(id=9, title="t", description="d")
    author = "user1"
    body = None
    with pytest.raises(TypeError):
        ticket.add_comment(body=body, author=author)

# TC10: 著者名がNone型（型違いエラー）
def test_add_comment_author_none():
    # TC10
    ticket = Ticket(id=10, title="t", description="d")
    author = None
    body = "テストコメント"
    with pytest.raises(TypeError):
        ticket.add_comment(body=body, author=author)

# TC11: 本文がint型の場合（型違いエラー）
def test_add_comment_body_int():
    # TC11
    ticket = Ticket(id=11, title="t", description="d")
    author = "user1"
    body = 123
    with pytest.raises(TypeError):
        ticket.add_comment(body=body, author=author)

# TC12: 著者名がint型の場合（型違いエラー）
def test_add_comment_author_int():
    # TC12
    ticket = Ticket(id=12, title="t", description="d")
    author = 123
    body = "テストコメント"
    with pytest.raises(TypeError):
        ticket.add_comment(body=body, author=author)

# TC13: 本文がlist型の場合（型違いエラー）
def test_add_comment_body_list():
    # TC13
    ticket = Ticket(id=13, title="t", description="d")
    author = "user1"
    body = ["a", "b"]
    with pytest.raises(TypeError):
        ticket.add_comment(body=body, author=author)

# TC14: 著者名がlist型の場合（型違いエラー）
def test_add_comment_author_list():
    # TC14
    ticket = Ticket(id=14, title="t", description="d")
    author = ["a", "b"]
    body = "テストコメント"
    with pytest.raises(TypeError):
        ticket.add_comment(body=body, author=author)

# TC15: 連続でコメント追加時のid増加確認（2件目の追加）
def test_add_comment_id_increment():
    # TC15
    ticket = Ticket(id=15, title="t", description="d")
    author = "user1"
    body1 = "テストコメント"
    body2 = "2件目のコメント"
    comment1 = ticket.add_comment(body=body1, author=author)
    comment2 = ticket.add_comment(body=body2, author=author)
    assert comment1.id == 1
    assert comment2.id == 2
    assert ticket.comments[-2] == comment1
    assert ticket.comments[-1] == comment2

# TC16: 本文が空白のみの文字列
def test_add_comment_body_whitespace():
    # TC16
    ticket = Ticket(id=16, title="t", description="d")
    author = "user1"
    body = "    "
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment

# TC17: 著者名が空白のみの文字列
def test_add_comment_author_whitespace():
    # TC17
    ticket = Ticket(id=17, title="t", description="d")
    author = "    "
    body = "テストコメント"
    comment = ticket.add_comment(body=body, author=author)
    assert comment.body == body
    assert comment.author == author
    assert comment.id == 1
    assert ticket.comments[-1] == comment